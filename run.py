from main import app

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host = "127.0.0.1", port=9000)
    #app.run(host = "192.168.45.131", port=9000, debug=False)  # 포트포워딩: 7000, 8000, 9000
    #app.run(host = "0.0.0.0", port=9000) #, debug=False)