# OSL Data Science Projects Gallery

**Welcome to our Project Gallery!**

Here, you can explore a variety of data science
projects affiliated to the OSL Data Science Internship Program.
Each project showcased here utilizes open data and is freely available as
open-source, embodying our commitment to transparency and collaboration in
science.

<div class="container mt-4">
    <div class="row">
        {% for dash in dashboards %}
        <div class="col-md-12 col-lg-6 col-xl-4">
            <div class="card mb-4 p-0">
                <img src="{{ dash.image.strip() }}" class="card-img-top my-0" alt="{{ dash.title.strip() }}">
                <div class="card-body">
                    <h5 class="card-title">{{ dash.title.strip() }}</h5>
                    <p class="card-text">{{ dash.description.strip() }}</p>
                    <a href="/projects/{{ dash.slug }}/" class="btn btn-primary">View Dashboard</a>
                    <a href="{{ dash.source_code_url }}/" class="btn btn-dark">Source Code</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
