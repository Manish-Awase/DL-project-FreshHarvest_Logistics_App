import streamlit as st
from torchvision import transforms
from PIL import Image
from predict_damage import predict
st.title('🍓 FreshHarvest Logistics App')
uploaded_image=st.file_uploader("Upload an image",type=["jpg", "png"])
image_path="./temp_image.jpg"
# expand predicted output
def expand_this(text:str):
    expand_dic={
        'S':'Spoiled',
        'F':'Fresh'
     }
    ex,fruit=text.split('_')
    return fruit,expand_dic[ex]
resize=transforms.Compose([transforms.Resize(256)])

if uploaded_image :
    st.info('image uploaded')
    # st.image(uploaded_image,use_container_width=True)
    with open(image_path,'wb') as f:
        f.write(uploaded_image.getbuffer())
    img=Image.open(image_path).resize((600,350))
    st.image(img)
    # st.image(uploaded_image , caption="Uploaded File", use_container_width=True)
    # prediction
    pct,prediction_class= predict(image_path)
    Fruit,Status=expand_this(prediction_class)

    st.write("Fruit Status")
    if prediction_class[0]=='F':
        st.success(f'Fruit: {Fruit}\n\nStatus: {Status}\n\nConfidence: {pct*100:0.0f}%')
    else:
        st.warning(f'Fruit: {Fruit}\n\nStatus: {Status}\n\nConfidence: {pct * 100:0.0f}%')