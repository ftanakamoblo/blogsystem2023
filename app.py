from flask import Flask, request, abort, render_template, redirect, url_for, jsonify, flash
from firebase_admin import firestore, initialize_app, credentials, auth, exceptions
import os
import json

# Firebaseの初期化
cred_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
initialize_app(cred)


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        id_token = request.form.get('id_token')
        try:
            # IDトークンを検証する
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            # 認証に成功したら、ユーザー情報をセッションに保存するなどの処理を行う
            # 例: session['user_id'] = uid
            return redirect(url_for('home'))
        except exceptions.FirebaseError as e:
            # 認証に失敗した場合の処理
            flash('ログインに失敗しました。トークンが無効か、期限切れです。')
            return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Firebase Authenticationを使用して新規ユーザーを登録する
            user = auth.create_user(email=email, password=password)
            # 登録に成功したら、ホームページにリダイレクトする
            return redirect(url_for('home'))
        except exceptions.FirebaseError as e:
            # 登録に失敗した場合の処理
            flash('アカウントの作成に失敗しました。')
            return redirect(url_for('register'))

@app.route('/logout', methods=['POST'])
def logout():
    # ログアウトはクライアントサイドで行います
    # サーバーサイドでは、通常はセッションをクリアするなどの処理を行います
    return jsonify({'message': 'Successfully logged out'}), 200

@app.route('/topic_input', methods=['GET'])
def show_topic_input():
    return render_template('topic_input.html')

@app.route('/generate_article', methods=['POST'])
def generate_article():
    # トピックとキーワードをリクエストから取得
    topic = request.form.get('topic')
    keywords = request.form.get('keywords')
    
    # OpenAI APIを使用して記事を生成するロジックをここに実装
    # 生成された記事をデータベースに保存し、記事IDを取得する
    
    # 記事IDを使用して記事表示ページにリダイレクト
    return redirect(url_for('show_article', article_id=article_id))

@app.route('/show_article/<article_id>', methods=['GET'])
def show_article(article_id):
    # データベースから記事IDに基づいて記事を取得するロジックを実装
    # 例: article = get_article_by_id(article_id)
    
    # 記事のタイトルと内容をテンプレートに渡してレンダリング
    return render_template('article_display.html', article_title=article['title'], article_content=article['content'])

if __name__ == '__main__':
    app.run(debug=True)