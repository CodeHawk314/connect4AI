import tensorflow as tf

def Conv2D(filters, kernel_size):
  return tf.keras.layers.Conv2D(
      filters=filters, 
      kernel_size=kernel_size, 
      padding='same',
      kernel_regularizer=tf.keras.regularizers.l2(1e-3))

def Dense(output_size):
  return tf.keras.layers.Dense(
      output_size,
      kernel_regularizer=tf.keras.regularizers.l2(1e-3))

class ResnetIdentityBlock(tf.keras.Model):
  def __init__(self, filters, kernel_size):
    super(ResnetIdentityBlock, self).__init__(name='')
    
    self.conv2a = Conv2D(filters, kernel_size)
    self.bn2a = tf.keras.layers.BatchNormalization()

    self.conv2b = Conv2D(filters, kernel_size)
    self.bn2b = tf.keras.layers.BatchNormalization()

  def call(self, input, training=False):
    x = self.conv2a(input)
    x = self.bn2a(x, training=training)
    x = tf.nn.relu(x)

    x = self.conv2b(x)
    x = self.bn2b(x, training=training)

    x += input
    x = tf.nn.relu(x)

    return x

class ResidualTower(tf.keras.Model):
  def __init__(self, filters, kernel_size, num_blocks):
    super(ResidualTower, self).__init__(name='')

    self.resblocks = [ResnetIdentityBlock(filters, kernel_size) for _ in range(num_blocks)]
    
  def call(self, x, training=False):

    for resblock in self.resblocks:
      x = resblock(x)

    return x

class PolicyHead(tf.keras.Model):
  def __init__(self, filters, kernel_size, output_size):
    super(PolicyHead, self).__init__(name='')
    
    self.conv = Conv2D(filters, kernel_size)
    self.bn = tf.keras.layers.BatchNormalization()
    self.dense = Dense(output_size)

  def call(self, x, training=False):
    x = self.conv(x)
    x = self.bn(x, training=training)
    x = tf.nn.relu(x)
    
    x = self.dense(x)
    x = tf.nn.sigmoid(x)
    x = tf.keras.layers.Flatten()(x)

    return x

class ValueHead(tf.keras.Model):
  def __init__(self, filters, kernel_size, hidden_size, output_size):
    super(ValueHead, self).__init__(name='')
    
    self.conv = Conv2D(filters, kernel_size)
    self.bn = tf.keras.layers.BatchNormalization()
    self.hidden_dense = Dense(hidden_size)
    self.output_dense = Dense(output_size)

  def call(self, x, training=False):
    x = self.conv(x)
    x = self.bn(x, training=training)
    x = tf.nn.relu(x)

    x = tf.keras.layers.Flatten()(x)

    x = self.hidden_dense(x)
    x = tf.nn.relu(x)

    x = self.output_dense(x)
    x = tf.nn.tanh(x)

    return x

class AlphaZeroNNet(tf.keras.Model):
  def __init__(self):
    super(AlphaZeroNNet, self).__init__()

    self.conv = Conv2D(filters=256, kernel_size=3)
    self.bn = tf.keras.layers.BatchNormalization()

    self.residual_tower = ResidualTower(kernel_size=3, filters=256, num_blocks=5) #19)
    self.policy_head = PolicyHead(kernel_size=1, filters=2, output_size=73)
    self.value_head = ValueHead(kernel_size=1, filters=1, hidden_size=256, output_size=1)

  def call(self, x, training=False):
    x = self.conv(x)
    x = self.bn(x, training=training)
    x = tf.nn.relu(x)
    
    x = self.residual_tower(x)
    policy = self.policy_head(x)
    value = self.value_head(x)

    return {'policy': policy, 'value': value}

nnet = AlphaZeroNNet()

@tf.function
def log_loss(y_true, y_pred):
    return -tf.einsum('ij,ij->i', y_true, tf.math.log(y_pred))

print(nnet.predict(tf.random.uniform([4, 8, 8, 17])))
nnet.summary()

nnet.compile(
    optimizer=tf.keras.optimizers.SGD(),
    loss={
        'policy': log_loss, # -pi * log(p)
        'value': tf.keras.losses.MeanSquaredError()}) # (z - v)^2

# Commented out IPython magic to ensure Python compatibility.
for n in range(8, 64, 8):
  print(n)
# %time nnet.evaluate(x=tf.random.uniform([n, 8, 8, 17]), y={'policy': tf.random.uniform([n, 8*8*73]), 'value': tf.random.uniform([n, 1])}, return_dict=True)