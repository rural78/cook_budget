from flask import Flask, redirect, render_template, request, session, url_for
import google.generativeai as genai
import csv
import pandas as pd
import re
import csv_to_pandas

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

@app.route('/', methods = ['get','post'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        GOOGLE_API_KEY="AIzaSyBQNVnxzVcR5dmS2DZ_B-GriOEw4o5h3GY"
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_pro = genai.GenerativeModel("gemini-pro")
        prompt=f"{session['name']}1人分の材料と分量(kg)をcsvで出力してください.ヘッダーは省略します.数値は,小数で入力します.1列目に材料を,2列目に分量を記述します.ただし,分量は,単位を省略してください.なお,材料に肉が含まれる場合,牛肉,豚肉,合挽肉,鶏肉の4種類の中から1種類を選択し,使用するものとします.ただし,肉以外の材料は,すべてカタカナ表記してください."
        #prompt = f"{session['name']}一人分の材料とその重さをcsv形式で返してください.ヘッダーは省略してください.なお料理中で使用する肉は牛肉，豚肉，合挽肉，鶏肉の4種類のうちいずれか一つ，または組み合わせのうちもっとも適切なものを使用してください."
        response = gemini_pro.generate_content(prompt)
        result = response.text
        #print(result)
        price = 0
#        session["price"] = price

        #session['result'] = response.text
        
        with open ("result.csv", "w", encoding = "utf-8") as f:
            #writer = csv.writer(f)
            #writer.writerows([[result]])
            f.write(result)

        session["material_budget"] = csv_to_pandas.budget_check()
        return redirect(url_for('registered'))
    return render_template('form.html')

"""""""""       
        with open ("result.csv", "r", encoding = "utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                with open ("all_material_new.csv","r") as material_f:
                    reader_material = csv.reader(material_f)
                    for row2 in reader_material:
                        #print(row)
                        #print(row2)
                        if len(row) != 0:
                            if (len(row) != 0) and (row[0] == row2[3]):
                                ##print(row[0])
                                print(row2[3])
                                #print(row[1])
                                #print(row2[7])
                                material_price = 0
                                material_price = float(row[1]) * float(row2[10])
                                ##print(material_price)
                                price += material_price
                                ##print(price)
  
session["price"] = int(price/0.6)
"""""""""
#                    for row in reader[]
@app.route('/registered')
def registered():
    return render_template('registered.html')


if __name__ == '__main__':
    app.run(debug = 'True', port = 8000)