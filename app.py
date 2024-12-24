import streamlit as st

from datasets import load_datasets, get_dataset_metadata
from visualization import single_plot_line_chart, stacked_bar_chart

datasets = load_datasets()
DATASET_METADATA = get_dataset_metadata()

# SIDEBAR
st.sidebar.title("Kelompok 9")
st.sidebar.text("1. Arifki Ilham (1301210405)\n2. Atha Ahsan Xavier Haris (1301210045)\n3. Farrel Arkana Veda (1301213138)")

selected_dataset_name = st.sidebar.selectbox(
    "Pilih dataset untuk ditampilkan:",
    [DATASET_METADATA[key]["name"] for key in DATASET_METADATA.keys()]
)
selected_key = [key for key, value in DATASET_METADATA.items() if value["name"] == selected_dataset_name][0]

# FILTERS
year_filter = st.sidebar.slider(
    "Filter Tahun",
    min_value=int(datasets[selected_key]["tahun"].min()),
    max_value=int(datasets[selected_key]["tahun"].max()),
    value=(
        int(datasets[selected_key]["tahun"].min()),
        int(datasets[selected_key]["tahun"].max())
    )
)
province_filter = st.sidebar.selectbox(
    "Pilih Provinsi:",
    options=["Seluruh Provinsi"] + list(datasets[selected_key]["provinsi"].unique())
)

filtered_data = datasets[selected_key][
    (datasets[selected_key]["tahun"].between(year_filter[0], year_filter[1]))
]
if province_filter != "Seluruh Provinsi":
    filtered_data = filtered_data[filtered_data["provinsi"] == province_filter]

# MAIN PAGE
st.title("Kesejahteraan Pekerja Indonesia")
st.image("./images/scenery_1.png", use_container_width=True)
st.markdown("[Dataset](https://www.kaggle.com/datasets/rezkyyayang/pekerja-sejahtera)")
st.text("Sebagai individu yang baru memulai karier, berbagai pertimbangan sering muncul, seperti lokasi tempat kerja, besaran gaji yang diterima, hingga kecukupan pendapatan untuk memenuhi kebutuhan sehari-hari. Mengacu pada data dari Badan Pusat Statistik (BPS), dashboard ini dirancang untuk membantu pekerja memilih lokasi kerja yang tepat dengan mempertimbangkan faktor seperti pendapatan dan pengeluaran. Dashboard ini memiliki relevansi tinggi mengingat persaingan di dunia kerja yang semakin ketat, sehingga perencanaan yang matang menjadi hal krusial, termasuk memastikan kesejahteraan pekerja melalui keputusan yang tepat.")

st.title("Eksplorasi Dataset")
st.subheader(f"Data: {selected_dataset_name}")
st.markdown(DATASET_METADATA[selected_key]["description"])

st.subheader("Ringkasan Statistik")
st.write(f"Total Baris: {filtered_data.shape[0]} | Total Kolom: {filtered_data.shape[1]}")
st.table(filtered_data.describe())

st.subheader(f"Dataset {province_filter.title()}")
st.dataframe(filtered_data, height=250, use_container_width=True)

st.download_button(
    label=f"Download Filtered {province_filter.title()}",
    data=filtered_data.to_csv(index=False),
    file_name=f"{selected_key}_filtered.csv",
    mime="text/csv"
)

st.subheader("Visualisasi Data")
if province_filter != "Seluruh Provinsi":
    if "tahun" in filtered_data.columns and selected_key in filtered_data.columns:
        if "jenis" in filtered_data.columns:
            chart_data = filtered_data.where(filtered_data["jenis"] == "TOTAL").groupby("tahun").mean(numeric_only=True).reset_index()
        else:
            chart_data = filtered_data.groupby("tahun").mean(numeric_only=True).reset_index()

        fig = single_plot_line_chart(
            data=chart_data,
            x="tahun",
            y=selected_key,
            title=DATASET_METADATA[selected_key]["name"],
            y_label=DATASET_METADATA[selected_key]["name"],
            dataset_name=selected_dataset_name
        )

        st.plotly_chart(fig, use_container_width=True)

    if "jenis" in filtered_data.columns:
        filtered_jenis_data = filtered_data[filtered_data["jenis"] != "TOTAL"]
        grouped_data = filtered_jenis_data.groupby(["tahun", "jenis"]).mean(numeric_only=True).reset_index()
        fig = stacked_bar_chart(
            data=grouped_data,
            x="tahun",
            y=selected_key,
            color="jenis",
            title=f"{DATASET_METADATA[selected_key]['name']} dengan Makanan dan Nonmakanan",
            labels={selected_key: DATASET_METADATA[selected_key]["name"], "tahun": "Tahun", "jenis": "Jenis Pengeluaran"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
else:
    for year in range(year_filter[0], year_filter[1] + 1):
        yearly_data = datasets[selected_key][datasets[selected_key]["tahun"] == year]
    
        
        if not yearly_data.empty: 
            chart_data = yearly_data.groupby("provinsi").mean(numeric_only=True).reset_index()
            
            chart_data = chart_data.sort_values(by=selected_key, ascending=False)

            fig = stacked_bar_chart(
                data=chart_data,
                x="provinsi",
                y=selected_key,
                color=None,
                title=f"Data Tahun {year} untuk Seluruh Provinsi",
                labels={"provinsi": "Provinsi", selected_key: DATASET_METADATA[selected_key]["name"]}
            )
            st.plotly_chart(fig, use_container_width=True)