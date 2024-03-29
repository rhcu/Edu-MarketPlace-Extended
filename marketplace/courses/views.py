from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import CourseForm, CourseEntryForm, LessonSaveForm, VideoSaveForm, AssignmentSaveForm, AssignmentSubmitForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from decimal import Decimal

import json
from datetime import date
import subprocess
import simplejson
from django.utils import translation

from .certificate import get_template
from .models import Course, CourseEntry, Lesson, Video, CourseEnroll, Quiz, Question
from .models import Answer, CourseProgression, UserAnswer, UserQuizPassed, Assignment, ChatMessage


def is_course_owner(course, user):
    return course.owner == user


def is_user_enrolled(course, user):
    if not user or not user.is_authenticated:
        return False
    if course.owner == user:
        return True
    enroll_count = CourseEnroll.objects.filter(course=course, user=user).count()
    return enroll_count > 0


def get_course(course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    return course


def get_lesson(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Lesson.objects.filter(course_entry=course_entry)[0]


def get_video(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Video.objects.filter(course_entry=course_entry)[0]


def get_quiz(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Quiz.objects.filter(course_entry=course_entry)[0]


def get_assignment(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Assignment.objects.filter(course_entry=course_entry)[0]


def index(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    userdata = {}
    user = request.user
    if user.is_authenticated:
        course_objects = Course.objects.all()
    else:
        course_objects = Course.objects.all()
    courses = []
    if user.is_authenticated:
        user = request.user
        auth0user = user.social_auth.get(provider='auth0')
        userdata = {
            'user_id': auth0user.uid,
            'name': user.first_name,
            'picture': auth0user.extra_data['picture'],
            'email': auth0user.extra_data['email'],
        }
    for course in course_objects:
        courses.append(
            (course, (is_user_enrolled(course, user), is_course_owner(course, user))))
    return render(request, 'courses.html', {
        'userdata': userdata,
        'courses': courses,
    })


def is_course_entry_completed(user, course, course_entry):
    course_progression = CourseProgression.objects.filter(user=user, course=course, course_entry=course_entry)
    if course_progression.count() == 0:
        progress = CourseProgression()
        progress.user = user
        progress.course = course
        progress.course_entry = course_entry
        progress.completed = False
        return False
    else:
        course_progression = course_progression[0]
        is_completed = getattr(course_progression, 'completed')
        return is_completed


@login_required
def add_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.date_created = timezone.now()
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'add_courses.html', {'form': form})


@login_required
def save_lesson(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    lesson = get_object_or_404(Lesson, pk=pk)
    course_entry = lesson.course_entry
    course = course_entry.course
    if user == course.owner:
        form = LessonSaveForm()
        form.fields['content'].initial = lesson.content
        if request.method == 'POST':
            form = LessonSaveForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lesson.content = cd.get('content', '')
                lesson.save()
                return redirect('lesson_detail', pk=course_entry.pk)
        return render(request, 'save_lesson.html', {'lesson': lesson, 'user': user, 'form': form})
    return redirect('course_detail', pk=course.pk)


@login_required
def lesson_detail(request, pk):
    # pk - primary key for course entry and NOT LESSON
    global lesson
    if request.user.is_authenticated:
        user = request.user
        lesson = get_lesson(pk)
        course_entry = lesson.course_entry
        course = course_entry.course
        if is_user_enrolled(lesson.course_entry.course, user):
            is_completed = is_course_entry_completed(user, course, course_entry)
            return render(request, 'lesson_detail.html', {'lesson': lesson, 'user': user, 'is_completed': is_completed})
    return redirect('course_detail', pk=lesson.course_entry.course.pk)


@login_required
def save_video(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    video = get_object_or_404(Video, pk=pk)
    course_entry = video.course_entry
    course = course_entry.course
    if user == course.owner:
        form = VideoSaveForm()
        form.fields['video_url'].initial = video.video_url
        if request.method == "POST":
            form = VideoSaveForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                video.video_url = cd.get("video_url", "")
                video.save()
                return redirect('video_detail', pk=course_entry.pk)
        return render(request, 'save_video.html', {'video': video, 'user': user, 'form': form})
    return redirect('course_detail', pk=course.pk)


@login_required
def video_detail(request, pk):
    # pk - primary key for course entry and NOT VIDEO
    global video
    if request.user.is_authenticated:
        user = request.user
        video = get_video(pk)
        course_entry = video.course_entry
        course = course_entry.course
        if is_user_enrolled(video.course_entry.course, user):
            is_completed = is_course_entry_completed(user, course, course_entry)
            return render(request, 'video_detail.html', {'video': video, 'user': user, 'is_completed': is_completed})
    return redirect('course_detail', pk=video.course_entry.course.pk)


@login_required
def save_question(request, quiz_pk):
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner:
        if request.method == 'POST':
            name = request.POST.get('name', '')
            pk = request.POST.get('pk', None)
            if pk:
                # Change question name, if it already exists
                question = get_object_or_404(Question, pk=pk)
            else:
                question = Question()
            question.name = name
            question.quiz = quiz
            question.save()
            obj = serializers.serialize('json', [question])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def save_answer(request, question_pk):
    if request.user.is_authenticated:
        user = request.user
    question = get_object_or_404(Question, pk=question_pk)
    quiz = get_object_or_404(Quiz, pk=question.quiz.pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner:
        if request.method == 'POST':
            name = request.POST.get('name', '')
            correct = 'true' in request.POST.get('correct')
            pk = request.POST.get('pk', None)
            if pk:
                # Change answer name, if it already exists
                answer = get_object_or_404(Answer, pk=pk)
            else:
                answer = Answer()
            answer.name = name
            answer.correct = correct
            answer.question = question
            answer.save()
            obj = serializers.serialize('json', [answer])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def user_passed_quiz(request, quiz_pk):
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if is_user_enrolled(course, user):
        if request.method == 'POST':
            quiz_passed = UserQuizPassed()
            quiz_passed.user = user
            quiz_passed.quiz = quiz
            quiz_passed.save()
            # Update quiz progression
            quiz_progress = CourseProgression.objects.filter(
                user=user, course=course, course_entry=course_entry).all()[0]
            quiz_progress.completed = True
            quiz_progress.save()
            obj = serializers.serialize('json', [quiz_passed])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def add_user_answer(request, answer_pk):
    if request.user.is_authenticated:
        user = request.user
    answer = get_object_or_404(Answer, pk=answer_pk)
    course = answer.question.quiz.course_entry.course
    if is_user_enrolled(course, user):
        if request.method == 'POST':
            correct = 'true' in request.POST.get('correct')
            user_answer = UserAnswer()
            user_answer.user = user
            user_answer.answer = answer
            user_answer.correct = correct
            user_answer.save()
            obj = serializers.serialize('json', [user_answer])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def get_user_answer(request, answer_pk):
    if request.user.is_authenticated:
        user = request.user
    answer = get_object_or_404(Answer, pk=answer_pk)
    course = answer.question.quiz.course_entry.course
    if is_user_enrolled(course, user):
        user_answer = get_object_or_404(UserAnswer, answer=answer)
        if user_answer.user == user or course.owner == user:
            # Only users themselves or course admin
            # can see their answers for privacy reasons
            obj = serializers.serialize('json', [user_answer])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def quiz_detail(request, pk):
    # pk - primary key for course entry and NOT QUIZ
    if request.user.is_authenticated:
        user = request.user
        quiz = get_quiz(pk)
        if is_user_enrolled(quiz.course_entry.course, user):
            user_passed_quiz = UserQuizPassed.objects.filter(quiz=quiz, user=user).count() > 0
            return render(request, 'quiz_detail.html', {'quiz': quiz, 'user': user, 'user_passed_quiz': user_passed_quiz})
    return redirect('course_detail', pk=quiz.course_entry.course.pk)


@login_required
def get_quiz_content(request, quiz_pk):
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if is_user_enrolled(course, user):
        if request.method == 'GET':
            questions = Question.objects.filter(quiz=quiz)
            arr_questions = []
            for question in questions:
                answers = Answer.objects.filter(question=question)
                arr_answers = []
                for answer in answers:
                    dict_answer = {'name': answer.name, 'pk': answer.pk}
                    if user == course.owner:
                        dict_answer['correct'] = answer.correct
                    if UserQuizPassed.objects.filter(quiz=quiz, user=user).count() > 0:
                        dict_answer['user_answer'] = UserAnswer.objects.filter(user=user, answer=answer)[0].correct
                        dict_answer['user_answered_correct'] = dict_answer['user_answer'] == answer.correct
                    arr_answers.append(dict_answer)
                dict_question = {'answers': arr_answers, 'name': question.name, 'pk': question.pk}
                arr_questions.append(dict_question)
            return JsonResponse({'questions': arr_questions})
    return redirect('course_detail', pk=course.pk)


@login_required
def save_quiz(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner:
        return render(request, 'save_quiz.html', {'quiz': quiz, 'user': user})
    return redirect('course_detail', pk=course.pk)


def update_progression(course, course_entry):
    entries = CourseEnroll.objects.filter(course=course)
    for entry in entries:
        progress = CourseProgression()
        progress.user = entry.user
        progress.course = entry.course
        progress.course_entry = course_entry
        progress.completed = False
        progress.save()


@login_required
def add_entry(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if user == course.owner:
        if request.method == 'POST':
            form = CourseEntryForm(request.POST)
            if form.is_valid():
                course_entry = form.save(commit=False)
                course_entry.date_created = timezone.now()
                course_entry.course = course
                course_entry.save()
                # Update CourseProgression data
                update_progression(course, course_entry)
                if course_entry.entry_type == 'lesson':
                    lesson = Lesson()
                    lesson.course_entry = course_entry
                    lesson.content = 'Here goes the content of your lesson!'
                    lesson.save()
                    return redirect('save_lesson', pk=lesson.pk)
                elif course_entry.entry_type == 'video':
                    video = Video()
                    video.course_entry = course_entry
                    video.save()
                    return redirect('save_video', pk=video.pk)
                elif course_entry.entry_type == 'quiz':
                    quiz = Quiz()
                    quiz.course_entry = course_entry
                    quiz.save()
                    return redirect('save_quiz', pk=quiz.pk)
                elif course_entry.entry_type == 'assignment':
                    assignment = Assignment()
                    assignment.course_entry = course_entry
                    assignment.user = user
                    assignment.is_course_owner = True
                    assignment.description = 'Describe assignment requirements here.'
                    assignment.save()
                    return redirect('save_assignment', pk=course_entry.pk)
                else:
                    raise Exception('Course entry is not found')
        else:
            form = CourseEntryForm()
        return render(request, 'add_entry.html', {'course': course, 'user': user, 'form': form})
    else:
        return redirect('course_detail', pk=course.pk)


def course_certificate(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_entries = CourseEntry.objects.filter(course=course)
    user = None
    course_progression = {}
    if request.user.is_authenticated:
        user = request.user
    user_enrolled = is_user_enrolled(course, user)
    if user_enrolled:
        course_entries_count = CourseProgression.objects.filter(user=user, course=course).count()
        course_entries_completed = CourseProgression.objects.filter(user=user, course=course, completed=True).count()
        
        if course_entries_completed < course_entries_count:
            return redirect('course_detail', pk=course.pk)
        certificate_id = str(course.pk) + "_" + str(user.pk)
        certificate_content = get_template(user.first_name, course.title, date.today().strftime("%d/%m/%Y"), certificate_id.replace("_", ""), course.owner.first_name)
        certificate_file = open(certificate_id + ".tex", "w")
        certificate_file.write(certificate_content)
        certificate_file.close()
        subprocess.run(["./laton", certificate_id + ".tex"])
        pdf_file = open(certificate_id + ".pdf", "rb")
        import mimetypes
        mime_type_guess = mimetypes.guess_type(certificate_id + ".pdf")
        response = HttpResponse(pdf_file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + certificate_id + '.pdf'
        return response
    return redirect('course_detail', pk=course.pk)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_entries = CourseEntry.objects.filter(course=course)
    user = None
    course_progression = {}
    if request.user.is_authenticated:
        user = request.user
    user_enrolled = is_user_enrolled(course, user)
    if user_enrolled:
        course_progression = CourseProgression.objects.filter(user=user, course=course)
    return render(request, 'course_detail.html',
                  {'course': course, 'user': user, 'course_entries': course_entries, 'user_enrolled': user_enrolled,
                   'course_progression': course_progression})


@login_required
def course_chat(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = None
    if request.user.is_authenticated:
        user = request.user
    is_owner = is_course_owner(course, user)
    user_enrolled = is_user_enrolled(course, user)
    if user_enrolled or is_owner:
        return render(request, 'course_chat.html',{
            'course': course,
            'user': user,
        })
    else:   
        return redirect('course_detail', pk=course.pk)

@login_required
def save_chat_message(request):
    if request.method == 'POST':
        # Save data to the ChatMessage table
        enroll = ChatMessage()
        enroll.handle = request.POST.get('handle')
        enroll.text = request.POST.get('text')
        enroll.chatId = request.POST.get('chatId')
        enroll.save()
    return HttpResponse("Saved!")

@login_required
def get_chat_message(request, pk):
    messages = ChatMessage.objects.filter(chatId=pk)
    obj = serializers.serialize('json', messages)
    return HttpResponse(obj, content_type="text/json-comment-filtered")


@login_required
def course_pay(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user
    return render(request, 'course_pay.html', {'course': course, 'user': user})    


@login_required
def course_enroll(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        # Save data to the CourseEnroll table
        enroll = CourseEnroll()
        enroll.user = user
        enroll.course = course
        enroll.save()
        # Save data to the CourseProgression table
        course_entries = CourseEntry.objects.filter(course=course)
        for course_entry in course_entries:
            progress = CourseProgression()
            progress.user = user
            progress.course = course
            progress.course_entry = course_entry
            progress.completed = False
            progress.save()
    # In any case, just redirect to course detail
    return redirect('course_detail', pk=course.pk)


@login_required
def course_unenroll(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    CourseEnroll.objects.filter(user=user, course=course).delete()
    CourseProgression.objects.filter(user=user, course=course).delete()
    return redirect('course_detail', pk=course.pk)


@login_required
def enrolled_list(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if user == course.owner:
        enrolled_objects = CourseEnroll.objects.filter(course=course)
        users = [obj.user for obj in enrolled_objects]
        user_to_progress = {}
        for enrolled_user in users:
            course_progression = CourseProgression.objects.filter(user=enrolled_user, course=course)
            completed = 0
            total = course_progression.count()
            for entry in course_progression:
                if getattr(entry, 'completed'):
                    completed += 1
            if total > 0:
                progress = completed/total * 100
                user_to_progress[enrolled_user] = int(round(progress))
            else:
                user_to_progress[enrolled_user] = 0
        return render(request, 'enrolled_list.html',
                      {'user': user, 'course': course, 'user_to_progress': user_to_progress})
    else:
        return redirect('course_detail', pk=course.pk)


def get_user_detail(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
        'courses': Course.objects.filter(owner=user)
    }
    return render(request, 'user_courses.html', context)


def get_progress(request, course_pk):
    global user
    if request.user.is_authenticated:
        user = request.user
    course = get_course(course_pk)
    if is_user_enrolled(course, user):
        course_progression = CourseProgression.objects.filter(user=user, course=course)
        completed = 0
        total = course_progression.count()
        for entry in course_progression:
            if getattr(entry, 'completed'):
                completed += 1
        response_data = {
            'completed': completed,
            'total': total
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    return redirect('course_detail', pk=course.pk)


@login_required
def delete_lesson(request, pk):
    # pk - primary key for lesson
    global user
    if request.user.is_authenticated:
        user = request.user
    lesson = get_object_or_404(Lesson, pk=pk)
    course_entry = lesson.course_entry
    if user == course_entry.course.owner:
        CourseProgression.objects.filter(course_entry=course_entry).all().delete()
        CourseEntry.objects.filter(pk=course_entry.pk).all().delete()
        lesson.delete()
    return redirect('course_detail', pk=course_entry.course.pk)


@login_required
def delete_video(request, pk):
    # pk - primary key for video
    global user
    if request.user.is_authenticated:
        user = request.user
    video = get_object_or_404(Video, pk=pk)
    course_entry = video.course_entry
    if user == course_entry.course.owner:
        CourseProgression.objects.filter(course_entry=course_entry).all().delete()
        CourseEntry.objects.filter(pk=course_entry.pk).all().delete()
        video.delete()
    return redirect('course_detail', pk=course_entry.course.pk)


@login_required
def mark_lesson(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    lesson = get_object_or_404(Lesson, pk=pk)
    course_entry = lesson.course_entry
    course = course_entry.course
    if is_user_enrolled(course, user):
        lesson_progress = CourseProgression.objects.filter(user=user, course=course, course_entry=course_entry).all()[0]
        is_completed = getattr(lesson_progress, 'completed')
        lesson_progress.completed = not is_completed
        lesson_progress.save()
    return redirect('lesson_detail', pk=course_entry.pk)


@login_required
def mark_video(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    video = get_object_or_404(Video, pk=pk)
    course_entry = video.course_entry
    course = course_entry.course
    if is_user_enrolled(course, user):
        video_progress = CourseProgression.objects.filter(user=user, course=course, course_entry=course_entry).all()[0]
        is_completed = getattr(video_progress, 'completed')
        video_progress.completed = not is_completed
        video_progress.save()
    return redirect('video_detail', pk=course_entry.pk)


@login_required
def get_course_rating(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_rating = course.rating
    response_data = {
        'value': simplejson.dumps(course_rating, use_decimal=True)
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def get_user_rating(request, course_pk):
    curr_user = None
    if request.user.is_authenticated:
        curr_user = request.user
    course = get_object_or_404(Course, pk=course_pk)
    if is_user_enrolled(course, curr_user):
        enrolled_course = CourseEnroll.objects.filter(user=curr_user, course=course).all()[0]
        user_rating = enrolled_course.user_rating
        response_data = {
            'value': simplejson.dumps(user_rating, use_decimal=True)
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    return redirect('course_detail', pk=course.pk)


@login_required
def set_course_rating(request, course_pk, rating):
    rating = int(rating)
    if rating // 10 > 0:
        rating /= 10
        rating = Decimal(rating)
    curr_user = None
    if request.user.is_authenticated:
        curr_user = request.user
    course = get_object_or_404(Course, pk=course_pk)
    if is_user_enrolled(course, curr_user):
        enrolled_course = CourseEnroll.objects.filter(user=curr_user, course=course).all()[0]
        enrolled_course.user_rating = rating
        enrolled_course.save()

        # User can rate a course once only, so we are safe to update the course rating like on the lines below
        enrolled_objects = CourseEnroll.objects.filter(course=course)
        count = 0
        total = 0
        for enrolled_object in enrolled_objects:
            if enrolled_object.user_rating != 0.0:
                total += enrolled_object.user_rating
                count += 1
        floor = total//count
        float_div = total/count - floor

        course_rating = floor
        if float_div > 0.5:
            course_rating = floor + 1
        elif float_div == 0.5:
            course_rating = floor + 0.5
        course.rating = course_rating
        course.save()
    return redirect('course_detail', pk=course.pk)


@login_required
def save_assignment(request, pk):
    # pk - primary key for course entry
    request_user = None
    if request.user.is_authenticated:
        request_user = request.user
    assignment = get_assignment(pk)
    course_entry = assignment.course_entry
    course = course_entry.course
    if request_user == course.owner:
        form = AssignmentSaveForm()
        form.fields['description'].initial = assignment.description
        if request.method == "POST":
            form = AssignmentSaveForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                assignments = Assignment.objects.filter(course_entry=course_entry).all()
                for assignment in assignments:
                    assignment.description = cleaned_data.get('description', '')
                    assignment.save()
                return redirect('assignment_detail', pk=course_entry.pk)
        return render(request, 'save_assignment.html',
                      {'assignment': assignment, 'user': request_user, 'form': form})
    return redirect('course_detail', pk=course.pk)


@login_required
def delete_assignment_entry(request, pk):
    # pk - primary key for course entry
    request_user = None
    if request.user.is_authenticated:
        request_user = request.user
    assignment = get_assignment(pk)
    course_entry = assignment.course_entry
    if request_user == course_entry.course.owner:
        CourseProgression.objects.filter(course_entry=course_entry).all().delete()
        assignments = Assignment.objects.filter(course_entry=course_entry).all()
        for assignment in assignments:
            assignment.delete()
        CourseEntry.objects.filter(pk=course_entry.pk).all().delete()
    return redirect('course_detail', pk=course_entry.course.pk)


# Deletes specific assignment
@login_required
def delete_assignment(request, pk):
    # pk - primary key for a specific assignment
    if request.user.is_authenticated:
        request_user = request.user
        if request.method == 'POST':
            assignment = Assignment.objects.get(pk=pk)
            course_entry = assignment.course_entry
            course = course_entry.course
            if request_user == course.owner:
                assignment.delete()
        return redirect('assignment_detail', pk=course_entry.pk)


@login_required
def assignment_detail(request, pk):
    # pk - primary key for course entry and NOT assignment
    if request.user.is_authenticated:
        request_user = request.user
        assignment = get_assignment(pk)
        course_entry = assignment.course_entry
        course = course_entry.course
        if request_user != course.owner and is_user_enrolled(course, request_user):
            is_completed = is_course_entry_completed(request_user, course, course_entry)
            if is_completed:
                return render(request, 'assignment_detail.html',
                              {'assignment': assignment, 'user': request_user, 'is_completed': is_completed,
                               'form': None})
            else:
                if request.method == 'POST':
                    # Create a new Assignment instance but do not save it yet
                    student_assignment = Assignment()
                    student_assignment.course_entry = course_entry
                    student_assignment.description = assignment.description
                    student_assignment.user = request_user
                    # Base an Assignment data from form on the Assignment instance created above
                    assignment_from_form = AssignmentSubmitForm(
                        request.POST, request.FILES, instance=student_assignment)
                    if assignment_from_form.is_valid():
                        # Save new Assignment instance
                        assignment_from_form.save()
                        # Auto-mark this course entry as completed for the current user
                        assignment_to_mark_progress = CourseProgression.objects.filter(
                            user=request_user, course=course, course_entry=course_entry).all()[0]
                        assignment_to_mark_progress.completed = True
                        assignment_to_mark_progress.save()
                        return render(
                            request, 'assignment_detail.html',
                            {'assignment': assignment, 'user': request_user, 'is_completed': True, 'form': None})
                else:
                    form = AssignmentSubmitForm()
                    return render(request, 'assignment_detail.html',
                                  {'assignment': assignment, 'user': request_user, 'is_completed': is_completed,
                                   'form': form})
        elif request_user == course.owner:
            assignments = Assignment.objects.filter(course_entry=course_entry).all()
            return render(request, 'assignment_detail.html',
                          {'assignment': assignment, 'assignments': assignments, 'user': request_user})
    course_entry = CourseEntry.objects.filter(pk=pk).all()[0]
    return redirect('course_detail', pk=course_entry.course.pk)
