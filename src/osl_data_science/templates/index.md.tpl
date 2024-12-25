# OSL Data Science Dashboard Gallery

<div class="container mt-4">
    <div class="row">
        {% for dash in dashboards %}
        <div class="col-md-4">
            <div class="card mb-4">
                <img src="{{ dash.image }}" class="card-img-top" alt="{{ dash.title }}">
                <div class="card-body">
                    <h5 class="card-title">{{ dash.title }}</h5>
                    <a href="dashboards/{{ dash.slug }}/" class="btn btn-primary">View Dashboard</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
