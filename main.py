import bs4
from selenium import webdriver
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    search_string = request.form['search_string']
    url = r'https://www.monsterindia.com/srp/results?query=' + search_string

    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(30)
    source = driver.page_source
    html = bs4.BeautifulSoup(source, 'html.parser')

    big_box = html.findAll('div', {'class': 'card-apply-content'})
    job_list = []
    count = 1

    for box in big_box:
        try:
            job_title = box.find('div', {'class': 'job-tittle'}).h3.a.text
            job_link = box.find('div', {'class': 'job-tittle'}).h3.a['href']
            location = box.find('div', {'class': 'job-tittle'}).div.div.span.small.text.strip()
            company = box.find('span', {'class': 'company-name'}).text.strip()
            experience = box.find('div', {'class': 'exp col-xxs-12 col-sm-3 text-ellipsis'}).text.strip()
            skills = box.find('p', {'class': 'descrip-skills'}).text.strip().replace(' ', '').replace('\n', ' ')
            salary = box.find('div', {'class': 'package col-xxs-12 col-sm-4 text-ellipsis'}).small.text.strip()

            my_dict = dict(count=count, job_title=job_title, job_link=job_link,
                           location=location, company=company,
                           experience=experience, skills=skills, salary=salary)

            job_list.append(my_dict)

            count += 1

            # print('Job Title -> ', job_title)
            # print('Job Link -> ', job_link)
            # print('Job Location -> ', location)
            # print('Company -> ', company)
            # print('Experience -> ', experience)
            # print(skills)
            # print('Salary -> ', salary)
            # print('-' * 50)
        except AttributeError:
            #         print('-'*50)
            continue

    return render_template('index.html', job_list=job_list)


if __name__ == '__main__':
    app.run(debug=True)