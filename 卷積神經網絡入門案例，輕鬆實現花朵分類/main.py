'''
環境：Tensorflow2 Python3.x 
''' 

import  matplotlib.pyplot  as  plt 
import  numpy  as  np 
import  os 
import  PIL 
import  tensorflow  as  tf 

from  tensorflow  import  keras 
from  tensorflow.keras  import  layers 
from  tensorflow.keras.models  import  Sequential 

#下載數據集
import  pathlib 
dataset_url =  "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
data_dir = tf.keras.utils.get_file( 'flower_photos' , origin=dataset_url, untar= True ) 
data_dir = pathlib.Path(data_dir) 

#查看數據集圖片的總數量
image_count = len(list(data_dir.glob( '* /*.jpg' ))) 
print(image_count) 

#查看鬱金香tulips目錄下的第1張圖片；
 tulips = list(data_dir.glob( 'tulips/*' )) 
PIL.Image.open(str(tulips[ 0 ])) 

#定義加載圖片的一些參數，包括：批量大小、圖像高度、圖像寬度
batch_size =  32
 img_height =  180
 img_width =  180 

#將80％的圖像用於訓練
train_ds = tf.keras.preprocessing.image_dataset_from_directory( 
  data_dir , 
  validation_split=0.2 , 
  subset= "training" , 
  seed= 123 , 
  image_size=(img_height, img_width), 
  batch_size=batch_size) 

#將20％的圖像用於驗證
val_ds = tf.keras.preprocessing.image_dataset_from_directory( 
  data_dir, 
  validation_split= 0.2 , 
  subset = "validation" , 
  seed= 123 , 
  image_size=(img_height, img_width), 
  batch_size=batch_size) 

#打印數據集中花朵的類別名稱，字母順序對應於目錄名稱
class_names = train_ds.class_names 
print(class_names) 


#將像素的值標準化至0到1的區間內。
normalization_layer = layers.experimental.preprocessing.Rescaling( 1./ 255 ) 

#調用map將其應用於數據集：
 normalized_ds = train_ds.map( lambda  x, y: (normalization_layer(x), y)) 
image_batch, labels_batch = next(iter(normalized_ds)) 
first_image = image_batch[ 0 ] 
# Notice the pixels values are now in `[0,1]`.
 print(np.min(first_image), np.max(first_image)) 

#數據增強通過對已有的訓練集圖片隨機轉換（反轉、旋轉、縮放等），來生成其它訓練數據
data_augmentation = keras.Sequential( 
  [ 
    layers.experimental.preprocessing.RandomFlip( "horizo​​ntal" ,  
                                                 input_shape=(img_height,  
                                                              img_width, 
                                                              3)), 
    layers.experimental.preprocessing.RandomRotation( 0.1 ), 
    layers.experimental.preprocessing.RandomZoom( 0.1 ), 
  ] 
) 

#搭建網絡模型
model = Sequential([ 
  data_augmentation, 
  layers.experimental.preprocessing.Rescaling( 1. / 255 ), 
  layers.Conv2D( 16 ,  3 , padding= 'same' , activation= 'relu' ), 
  layers.MaxPooling2D(), 
  layers.Conv2D( 32 ,  3 , padding= 'same' , activation= 'relu' ),
  layers.MaxPooling2D(), 
  layers.Conv2D( 64 ,  3 , padding= 'same' , activation= 'relu' ), 
  layers.MaxPooling2D(), 
  layers.Dropout( 0.2 ), 
  layers.Flatten(), 
  layers.Dense( 128 , activation= 'relu' ), 
  layers.Dense(num_classes) 
]) 

#編譯模型
model.compile(optimizer= 'adam' , 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits= True ), 
              metrics=[ 'accuracy ' ]) 

#查看網絡結構
model.summary() 

#訓練模型
epochs =  15
 history = model.fit( 
  train_ds, 
  validation_data=val_ds, 
  epochs=epochs 
) 

#在訓練和驗證集上查看損失值和準確性
acc = history.history[ 'accuracy' ] 
val_acc = history.history[ 'val_accuracy ' ] 

loss = history.history[ 'loss' ] 
val_loss = history.history[ 'val_loss' ] 

epochs_range = range(epochs) 

plt.figure(figsize=( 8 ,  8 )) 
plt.subplot( 1 ,  2 ,  1 ) 
plt.plot(epochs_range, acc, label= 'Training Accuracy' )
plt.plot(epochs_range, val_acc, label= 'Validation Accuracy' ) 
plt.legend(loc= 'lower right' ) 
plt.title( 'Training and Validation Accuracy' ) 

plt.subplot( 1 ,  2 ,  2 ) 
plt.plot (epochs_range, loss, label= 'Training Loss' ) 
plt.plot(epochs_range, val_loss, label= 'Validation Loss' ) 
plt.legend(loc= 'upper right' ) 
plt.title( 'Training and Validation Loss' ) 
plt .show()