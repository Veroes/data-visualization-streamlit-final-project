import streamlit as st

from datasets import load_datasets, get_dataset_metadata
from visualization import single_plot_line_chart, stacked_bar_chart, geo_map

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
    options=list(datasets[selected_key]["provinsi"].unique())
)

filtered_data = datasets[selected_key][
    (datasets[selected_key]["tahun"].between(year_filter[0], year_filter[1]))
]
if province_filter != "":
    filtered_data = filtered_data[filtered_data["provinsi"] == province_filter]

# MAIN PAGE
st.title("Kesejahteraan Pekerja Indonesia")
st.markdown("[Dataset](https://www.kaggle.com/datasets/rezkyyayang/pekerja-sejahtera)")
st.text("Sebagai seseorang yang baru memasuki dunia kerja, seringkali muncul berbagai pertimbangan, seperti lokasi tempat bekerja, jumlah upah yang akan diterima, hingga apakah pendapatan tersebut cukup untuk memenuhi kebutuhan sehari-hari. Berdasarkan data yang diambil dari Badan Pusat Statistik (BPS), dashboard ini dirancang untuk membantu pekerja dalam menentukan lokasi kerja yang sesuai dengan mempertimbangkan variabel seperti pendapatan dan pengeluaran. Dashboard ini menjadi relevan karena persaingan dunia kerja yang semakin ketat, sehingga perencanaan yang matang sangat diperlukan, termasuk memastikan kesejahteraan pekerja berdasarkan keputusan yang diambil.")

# GEOMAP
geo_fig = geo_map(
    data_frame=datasets[selected_key],
    year=2017,
    location="provinsi",
    color=selected_key,
    title=f"Peta Sebaran {DATASET_METADATA[selected_key]['name']}",
)

st.plotly_chart(geo_fig, use_container_width=True)

st.title("Eksplorasi Dataset")
st.subheader(f"Data: {selected_dataset_name}")
st.markdown(DATASET_METADATA[selected_key]["description"])

st.subheader("Ringkasan Statistik")
st.write(f"Total Baris: {filtered_data.shape[0]} | Total Kolom: {filtered_data.shape[1]}"   )
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

if "daerah" in filtered_data.columns:
    filtered_daera_data = filtered_data[filtered_data["daerah"] != "TOTAL"]
    grouped_data = filtered_daera_data.groupby(["tahun", "daerah"]).mean(numeric_only=True).reset_index()

    fig = stacked_bar_chart(
        data=grouped_data,
        x="tahun",
        y=selected_key,
        color="daerah",
        title=f"{DATASET_METADATA[selected_key]['name']} dengan Perdesaan, Perkotaan",
        labels={selected_key: DATASET_METADATA[selected_key]["name"], "tahun": "Tahun", "daerah": "Daerah"}
    )
    
    st.plotly_chart(fig, use_container_width=True)