export VUE_APP_API_URL=http://localhost
export VUE_APP_API_PORT=8000
cd frontend
npm run build
cd ..
python build.py