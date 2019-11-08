from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
from keras import models
from keras import layers
from keras import optimizers
from matplotlib import pyplot as plt
import tensorflow as tf


sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input,
                                   zoom_range=0.4,
                                   #horizontal_flip=True,
                                   vertical_flip=True,
                                   brightness_range=[0.1, 0.7],
                                   fill_mode='nearest')

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

TRAIN_DIR = '/home/iref/Datasets/Kern_project/train'
VAL_DIR = '/home/iref/Datasets/Kern_project/val'
TEST_DIR = '/home/iref/Datasets/Kern_project/test'

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(100, 100),
    batch_size=16,
    class_mode='binary')

validation_generator = train_datagen.flow_from_directory(
    VAL_DIR,
    target_size=(100, 100),
    batch_size=8,
    class_mode='binary')

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(100, 100),
    batch_size=7,
    class_mode='binary'
)

conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(100, 100, 3))

model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.4))
model.add(layers.Dense(1, activation='sigmoid'))

conv_base.trainable = False

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.Adam(lr=2e-5),
              metrics=['acc'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch=27,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=6,
    verbose=2
)

model.save('vgg_dc.h5')

unfrozen = ['block5_conv1', 'block4_conv1']

conv_base.trainable = True
set_trainable = False
for layer in conv_base.layers:
    if layer.name in unfrozen:
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False
print('Number of trainable params after unfreezing: {}'.format(len(model.trainable_weights)))

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.Adam(lr=1e-6),
              metrics=['acc'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch=27,
    epochs=100,
    validation_data=validation_generator,
    validation_steps=6,
    verbose=2
)

model.save('vgg_full_v2.h5')

test_loss, test_acc = model.evaluate_generator(test_generator, steps=7)
print('test acc:', test_acc)

def smooth_curve(points, factor=0.8):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points


acc = history.history['acc']
loss = history.history['loss']
val_acc = history.history['val_acc']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)
plt.plot(epochs, smooth_curve(acc), 'bo', label='Smoothed training acc')
plt.plot(epochs, smooth_curve(val_acc), 'b', label='Smoothed validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, smooth_curve(loss), 'bo', label='Smoothed training loss')
plt.plot(epochs, smooth_curve(val_loss), label='Smoothed validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()