# OSL Data Science Dashboard Gallery

<div class="container mt-4">
    <div class="row">
        {% for dash in dashboards %}
        <div class="col-md-12 col-lg-6 col-xl-4">
            <div class="card mb-4 p-0">
                <img src="{{ dash.image.strip() }}" class="card-img-top my-0" alt="{{ dash.title.strip() }}">
                <div class="card-body">
                    <h5 class="card-title">{{ dash.title.strip() }}</h5>
                    <p class="card-text">{{ dash.description.strip() }}</p>
                    <a href="/dashboards/{{ dash.slug }}/" class="btn btn-primary">View Dashboard</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
