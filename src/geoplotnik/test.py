import dash
import dash_mantine_components as dmc
from dash import Dash, html

app = Dash(use_pages=True, pages_folder="")

dash.register_page("home", path="/", layout=html.Div("I'm home"))
dash.register_page("page1", path="/page-1", layout=html.Div("Info about page 1 subjects"))
dash.register_page("page1s1", path="/page-1/sub-1", layout=html.Div("page 1 subject 1"))
dash.register_page("page1s2", path="/page-1/sub-2", layout=html.Div("page 1 subject 2"))

component = dmc.Box([
    dmc.NavLink(label="home", href="/", active='exact'),
    dmc.NavLink(
            label="Page 1",
            childrenOffset=28,
            href="/page-1",
            active='partial',
            children=[
                dmc.NavLink(label="Subject 1", href="/page-1/sub-1", active="exact"),
                dmc.NavLink(label="Subject 2", href="/page-1/sub-2", active="exact"),
            ],
    ),
    dmc.Divider(mb="lg"),
    dash.page_container
])


app.layout = dmc.MantineProvider([component])

if __name__ == "__main__":
    app.run(debug=True)