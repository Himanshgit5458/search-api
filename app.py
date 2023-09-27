from flask import Flask, render_template, request, jsonify, send_file,Response
import pandas as pd
import io
from serpapi import GoogleSearch

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    query = request.form['query']
    country = request.form['country']
    location = request.form['location']
    device = request.form['device']

    # Replace the following code with your data processing logic
    # Sample code to create a DataFrame
    h1_list, h2_list, h3_list, description_list, extensions_list, same_searches_list = [], [], [], [], [], []
    params = {
            "engine": "google",
            "q": query,
            "api_key": "c49eef74b38411a5fcd322b22a02e024cf483d6374f6639ad9ad4b1568f6152a",
            "Country": country,
            "Language": "en",
            "location": location,
            "device": device,
        }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    # organic_results = results["organic_results"]
    related_searches = results["related_searches"]

    try:
        ads = results["ads"]
        for i in ads:
            try:
                headline = i["title"].split("-")
                if len(headline) == 2:
                    h1_list.append(headline[0])
                    h2_list.append(headline[1])
                    h3_list.append("")  # Add an empty string for missing h3
                elif len(headline) == 3:
                    h1_list.append(headline[0])
                    h2_list.append(headline[1])
                    h3_list.append(headline[2])
                else:
                    h1_list.append(i.get("title", ""))  # Use get method to handle missing title
                    h2_list.append("")
                    h3_list.append("")
            except:
                h1_list.append(i.get("title", ""))  # Use get method to handle missing title
                h2_list.append("")
                h3_list.append("")
            try:
                description_list.append(i.get("description", ""))  # Use get method to handle missing description
            except:
                description_list.append("")
            try:
                extensions_list.append(i.get("extensions", ""))  # Use get method to handle missing extensions
            except:
                extensions_list.append("")

        for i in related_searches:
            same_searches_list.append(i["query"])

        maxi=max(len(h1_list),len(h2_list),len(h3_list),len(description_list),len(extensions_list),len(same_searches_list) )
            
        h1_list += [""] * (maxi - len(h1_list))
        h2_list += [""] * (maxi - len(h2_list))
        h3_list += [""] * (maxi - len(h3_list))
        description_list += [""] * (maxi - len(description_list))
        extensions_list += [""] * (maxi - len(extensions_list))
        same_searches_list += [""] * (maxi - len(same_searches_list))


    # Process the data (you can modify this as needed)
        data2 = {"Headline -1":h1_list,"Headline -2":h2_list,"Headline -3":h3_list,"Description":description_list,"Extensions":extensions_list,"Similar Searches":same_searches_list}
        print(data2)

        
        # print(h1_list)
        df = pd.DataFrame(data2)

        # Generate a CSV file in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Create a downloadable CSV response
        response = Response(csv_buffer.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=result.csv'

        return response
    except:
        for i in related_searches:
            same_searches_list.append(i["query"])
            df = pd.DataFrame({"Similar Searches":same_searches_list})

        # Generate a CSV file in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Create a downloadable CSV response
        response = Response(csv_buffer.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=result.csv'

        return response


if __name__ == '__main__':
    app.run(debug=True)
