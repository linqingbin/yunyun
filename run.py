
from yunyun.route import app
from config import DEBUG

if __name__ == '__main__':
    app.run('0.0.0.0',7000,debug=DEBUG)
    