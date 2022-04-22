import sys
sys.path.insert(0,'/export/gladdb')
from app import app

if __name__ == "__main__":
    app.run(debug=False)
