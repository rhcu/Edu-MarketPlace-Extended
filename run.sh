(
  PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"

  cd $PROJECT_ROOT

  if [ "$BUILD_ENV" = "chat" ]; then
    echo "Here will be chat startup"
  else
    gunicorn --chdir marketplace/ marketplace.wsgi
  fi
)