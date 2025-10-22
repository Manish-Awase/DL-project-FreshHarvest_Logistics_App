import torch
from torchvision import transforms,models
from PIL import Image
from torch import nn
import torch.nn.functional as F

trained_model=None

class_names = ['F_Banana',
 'F_Lemon',
 'F_Lulo',
 'F_Mango',
 'F_Orange',
 'F_Strawberry',
 'F_Tamarillo',
 'F_Tomato',
 'S_Banana',
 'S_Lemon',
 'S_Lulo',
 'S_Mango',
 'S_Orange',
 'S_Strawberry',
 'S_Tamarillo',
 'S_Tomato']

# Define model

class ClassifierResNet(nn.Module):
    def __init__(self, num_classes=16, dropout_rate=0.5):
        super().__init__()
        # Load the pre-trained ResNet model
        self.model = models.resnet50(weights='DEFAULT')
        # Freeze all layers except the final fully connected layer
        for param in self.model.parameters():
            param.requires_grad = False

        # Unfreeze layer4 and fc layers
        for param in self.model.layer4.parameters():
            param.requires_grad = True

            # Replace the final fully connected layer
        self.model.fc = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.model.fc.in_features, num_classes)
        )

    def forward(self, x):
        x = self.model(x)
        return x



def predict(image_path):
    uploaded_img=Image.open(image_path).convert('RGB')
    transform_image=transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
    global trained_model


    # for transform and adding dimension in above image - [image]
    image_tensor = transform_image(uploaded_img).unsqueeze(0)
    if trained_model is None:
        trained_model=ClassifierResNet()
        # Load the pre-trained ResNet model
        trained_model.load_state_dict(torch.load("model/saved_model.pth",map_location=torch.device('cpu')))
        trained_model.eval()
    with torch.no_grad():

        prediction=trained_model(image_tensor)

        # prediction have [[]] so dim =(1,4) (for along column )in max

        probabilities = F.softmax(prediction, dim=1)

        # Step 2: Get top class and its confidence
        confidence_v, pred_class = torch.max(probabilities, dim=1)

    return confidence_v.item(), class_names[pred_class.item()]



