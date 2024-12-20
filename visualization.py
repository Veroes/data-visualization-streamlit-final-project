import plotly.express as px

def single_plot_line_chart(data, x, y, title, y_label, dataset_name):
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title + " di setiap Tahun",
        labels={x: "Tahun", y: y_label},
        markers=True
    )
    fig.update_layout(
        title=title + " di setiap Tahun",
        xaxis_title="Tahun",
        yaxis_title=dataset_name,
        xaxis=dict(tickmode='linear', tickangle=45),
        template="plotly_dark"
    )

    return fig

def stacked_bar_chart(data, x, y, color, title, labels):
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels,
        barmode="stack"
    )
    fig.update_layout(template="plotly_dark", xaxis=dict(tickmode='linear', tickangle=45))
    
    return fig