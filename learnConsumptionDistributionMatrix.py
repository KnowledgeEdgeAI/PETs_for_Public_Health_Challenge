import tensorflow as tf
from tensorflow.keras import Model

# Define the W parameter as a TensorFlow variable (trainable parameter)
m, n = 5, 5  # Dimensions of the matrix W (example: 5x5 matrix)
W = tf.Variable(initial_value=tf.random.normal([m, n]), trainable=True)

# Custom function to compute Y_pred from W
def custom_yij(W):
    # Get the shape of W
    m, n = W.shape
    
    # Create indices for i and j
    i_indices = tf.range(1, m + 1, dtype=tf.float32)[:, tf.newaxis]  # Shape [m, 1]
    j_indices = tf.range(1, n + 1, dtype=tf.float32)[tf.newaxis, :]  # Shape [1, n]
    
    # Compute Y_ij = i * j * W_ij
    Y_pred = i_indices * j_indices * W  # Element-wise multiplication
    return Y_pred

# Custom model: Define how Y_pred is computed based on W
class CustomModel(Model):
    def __init__(self, W):
        super(CustomModel, self).__init__()
        self.W = W  # Use W in the computation of Y_pred

    def call(self, inputs):
        # Use the custom function to compute Y_pred
        Y_pred = custom_yij(self.W)
        return Y_pred

# Define the Mean Squared Error (MSE) loss function
def mse_loss(Y_true, Y_pred):
    return tf.reduce_mean(tf.square(Y_true - Y_pred))

# Initialize model with the W parameter
model = CustomModel(W)

# Compile the model with the Adam optimizer and custom loss function
model.compile(optimizer='adam', loss=mse_loss)

# Suppose Y_true is the true matrix of values
Y_true = tf.random.normal([m, n])

# Train the model
model.fit(x=None, y=Y_true, epochs=1000)

# Get the trained W
trained_W = model.W.numpy()
