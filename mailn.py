import streamlit as st
st.title('기원~~~줴줴이야')
a=st.text_input('이름을 입력하세요!')
b=st.selectbox('좋아하는 단어를 입력하세요',['기원~~','엄줴줴이야ㅇ','티원~~'])
if st.button('인사말생성'):
  st.write('반가워요~')
