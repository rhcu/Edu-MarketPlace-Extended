(
  if [ "$BUILD_ENV" = "chat" ]; then
    echo "Here will be chat startup"
  else
    gunicorn --chdir marketplace/ marketplace.wsgi
  fi
)