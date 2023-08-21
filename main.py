import pandas as pd
import streamlit as st
import string
import pygwalker as pyg

def normalize_data(data):
    if isinstance(data, str):
        data = reduce_punctuation(data)  # Reduksi tanda baca
        data = data.strip().lower()
        data = data.title()
        return data
    else:
        return None

def reduce_punctuation(text):
    if isinstance(text, str):
        punctuation_set = set(string.punctuation)
        reduced_text = ''.join(char for char in text if char not in punctuation_set)
        return reduced_text
    else:
        return ""

def main():
    st.title("Aplikasi Analysis dan Normalisasi")
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        background-color: #000000   ;
        padding: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    menu = ["Normalisasi Data", "Analysis Data", "Unpivot Data","Contact"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)
    
    if choice == "Normalisasi Data":
        st.subheader("Aplikasi Normalissasi")
        st.write("Selamat datang di Aplikasi Normalisasi dan Analysis")
        uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])

        if uploaded_file is not None:
            # Membaca data dari file Excel
            data = pd.read_excel(uploaded_file, header=0)  # Set header=0 to use the top row as column names

            # Daftar kolom untuk normalisasi
            column_list = data.columns.tolist()
            selected_columns = st.multiselect("Pilih kolom untuk dinormalisasi", column_list)

            # Data yang belum ternormalisasi
            input_data = data[selected_columns]

            # Get the count of unique values before normalization
            unique_count_before = input_data.nunique()

            # Normalisasi data for each selected column
            normalized_data = {}
            for col in selected_columns:
                normalized_data[col] = input_data[col].apply(normalize_data)

            unique_count_after = {col: normalized_data[col].nunique() for col in selected_columns}

            # Menampilkan hasil normalisasi
            st.write("Data Sebelum Normalisasi")
            st.write(input_data)

            # Menampilkan jumlah data unique sebelum dan sesudah normalisasi
            st.write("Jumlah Data Unique Sebelum Normalisasi:", unique_count_before)
            st.write("Jumlah Data Unique Sesudah Normalisasi:", unique_count_after)
            
            result_df = pd.concat([input_data, pd.DataFrame(normalized_data)], axis=1)
            result_df = result_df.loc[:,~result_df.columns.duplicated()]

            csv = result_df.to_csv(index=False)
            st.download_button(
                label="Download Hasil Normalisasi",
                data=csv,
                file_name="hasil_normalisasi.csv",
                mime="text/csv"
            )

            # Show the DataFrame
            st.write("Data Hasil Normalisasi")
            st.dataframe(normalized_data)
            
    elif choice == "Analysis Data":
        st.subheader("Analysis Data")
        st.markdown('Silahkan Explore data Anda')
        
        uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])
        if uploaded_file is not None:
            data = pd.read_excel(uploaded_file)
            pyg.walk(data,env="Streamlit",dark='dark')
        
    elif choice == "Unpivot Data":
        st.subheader("Upivot data")
        uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])

        if uploaded_file is not None:
            # Membaca data dari file Excel
            data = pd.read_excel(uploaded_file, header=0)  # Set header=0 to use the top row as column names
            
            st.write("Data Awal:")
            st.dataframe(data)

            # Daftar kolom untuk unpivot
            column_list = data.columns.tolist()
            selected_columns = st.multiselect("Pilih kolom yang akan diunpivot", column_list)

            if selected_columns:
                id_vars = [col for col in column_list if col not in selected_columns]
                melted_data = pd.melt(data, id_vars=id_vars, value_vars=selected_columns, var_name="Kolom", value_name="Nilai")

                st.write("Data Hasil Unpivot:")
                st.dataframe(melted_data)

                    # Menyimpan hasil unpivot dengan label baru ke dalam file Excel
                st.write("Download Hasil Unpivot dengan Label Baru:")
                csv = melted_data.to_csv(index=False)
                st.download_button(
                    label="Download Hasil Unpivot dengan Label Baru",
                    data=csv,
                    file_name="hasil_unpivot_label_baru.csv",
                    mime="text/csv"
                )
    elif choice == "Contact":
        st.subheader("KKP UNIVERSITAS BUMIGORA 2023")
        st.write("Jika Anda memiliki pertanyaan, silakan hubungi kami di murdiantasriel@gmail.com")

    st.markdown('<div class="footer">KKP UNIVERSITAS BUMIGORA 2023</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
