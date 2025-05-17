from PIL import Image, ExifTags
import streamlit as st
import time

st.title('st.cache_dataの挙動確認アプリ')
st.text('わざと重ための画像を表示させて、@st.cache_dataがどう機能するかを確認するためのアプリです')
st.text('time.sleep(2)を画像読込関数に組み込んでいるため、キャッシュがない状態だと確実に2秒以上かかります')
st.text('一度表示した画像はキャッシュが残るため、比較的スムーズに表示されるはずです')
num = st.radio("ねこ画像を切り替えることができます", [1, 2, 3, 4], horizontal=True)

@st.cache_data(show_spinner='Now Loading...')
def imgLoad(n):
    time.sleep(2)
    return Image.open(f'{n}.JPG')

img = imgLoad(num)

exif_dict = img._getexif() # 画像のexifタグを取得する
tags = ExifTags.TAGS # ExifTagsのtagの名前を取得
exif_data = {} # 画像のexifデータとExifTagsのタグ名を組み合わせるためのdict
for key, value in exif_dict.items(): # exifデータとタグ名を組み合わせる
    exif_data[ExifTags.TAGS[key]] = value

# exifタグのorientationは画像の向きを表す。値によって角度を変更する
if "Orientation" in exif_data:
    ori = exif_data['Orientation']
    if ori == 3:
        img = img.rotate(180, expand=True)
    elif ori == 6:
        img = img.rotate(270, expand=True)
    elif ori == 8:
        img = img.rotate(270, expand=True)

st.image(img)
st.text('以下exifタグの情報です')
st.write(exif_data)