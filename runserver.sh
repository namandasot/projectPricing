while true; do
  echo "Re-starting Django runserver"
  python manage.py runserver 0.0.0.0:9100
  sleep 1
done
