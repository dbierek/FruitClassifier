
# Plotting Stuff:
#################
# def train():
#     history = train_model(4)
#     save_model()
#     # show_acc_and_loss(history)

# def next():
#     next_image()
#     # show_features()
# features_to_show = 4
# def pca_analysis():
#     test_generator_big.reset()
#     for x_batch, y_batch in test_generator_big:
#         data = x_batch
#         y_data = y_batch
#         break
#     data_flat = data.reshape(-1, 30000)
#     feat_cols = ['pixel' + str(i) for i in range(data_flat.shape[1])]
#     data_frame = pd.DataFrame(data_flat, columns=feat_cols)
#     y_data = [get_prediction_class(y_data[i]) for i in range(len(y_data))]
#     data_frame['label'] = y_data

#     print("Beginning PCA fitting:")
#     pca = PCA(n_components=2)
#     principal_components = pca.fit_transform(data_frame.iloc[:, :-1])
#     pc_dataframe = pd.DataFrame(data=principal_components, columns=['Principal Component 1', 'Principal Component 2'])
#     pc_dataframe['Fruit Type'] = y_data
#     print("Principal components data frame:")
#     print(pc_dataframe)
#     plt.figure(figsize=(16,10))
#     sns.scatterplot(
#         x="Principal Component 1", y="Principal Component 2",
#         hue="Fruit Type",
#         data=pc_dataframe
#     )
#     print('Explained Variation Ratio for each principal component: {}'.format(pca.explained_variance_ratio_))
#
# def plot_filters():
#     print("Plotting 3x3 Filters")
#     for layer in model.layers:
#         # Only show filters for 2d convolution layers
#         if "conv2d" not in layer.name:
#             continue
        
#         # Initialize the filters
#         filters, _ = layer.get_weights()
        
#         print("Layer:", layer.name, " Filter Shape:", filters.shape)
        
#         # Rescale filters from 0-1
#         filters_min = filters.min()
#         filters_max = filters.max()
#         filters = (filters - filters_min) / (filters_max - filters_min)
        
#         # Graph 8 filters for each layer
#         num_filters = 8
#         row = 1
        
#         # Create a figure for this model layer
#         plt.figure()
        
#         # Graph each filter
#         for filter_num in range(num_filters):
#             # Initialize filter_data to be each filter's data
#             filter_data = filters[:, :, :, filter_num]
            
#             # Show Red, Green, and Blue color channels for each filter
#             for channel in range(3):
#                 # Create a new subplot that is 3 columns wide for each filter
#                 subplot = plt.subplot(num_filters, 3, row)
#                 subplot.set_xticks([])
#                 subplot.set_yticks([])
#                 # Graph the Red, Green, and Blue channels of the filter
#                 plt.imshow(filter_data[:, :, channel], cmap='gray')
#                 row += 1
#         # After graphing, plt.show() must be called to display the graphs
#         plt.show()

# def show_features():
#     # Get the image path
#     img_path = get_image_path(cur_image_start)

#     # Load the image
#     img = load_img(img_path, target_size=(100, 100))
#     img = img_to_array(img)
#     img = expand_dims(img, axis=0)
#     img = preprocess_input(img)

#     # Show features for the first 6 layers
#     for layer_num in range(6):
#         # Get the model at each layer
#         print("Creating model for layer", layer_num)
#         layer_model = Model(inputs=model.inputs, outputs=model.layers[layer_num].output)
        
#         print("Making prediction for layer", layer_num)        
#         # Make a prediction of the features using this model
#         feature_maps = layer_model.predict(img)
#         print("Drawing feature maps for layer", layer_num)
#         # Create a new figure for these feature maps
#         plt.figure(figsize=(20,10))
#         for feature_map in feature_maps:
#             feature_num = 1
#             for _ in range(features_to_show):
#                 # Create a subplot for this feature map
#                 subplot = plt.subplot(1, 4, feature_num)
#                 subplot.set_xticks([])
#                 subplot.set_yticks([])
#                 # Show this feature map
#                 image = subplot.imshow(feature_map[:, :, feature_num - 2])
#                 feature_num += 1
#                 divider = make_axes_locatable(subplot)
#                 color_axis = divider.append_axes("right", size="5%", pad=0.1)

#                 # Show a color bar
#                 plt.colorbar(image, cax=color_axis)
#         # Show the features
#         plt.show()    
# def show_acc_and_loss(history):
#     accuracy = history.history['accuracy']
#     test_accuracy = history.history['val_accuracy']

#     loss = history.history['loss']
#     test_loss = history.history['val_loss']

#     # Get number of epochs
#     number_of_epochs = len(accuracy)
#     x = range(number_of_epochs)

#     # Create a figure for the Accuracy
#     plt.figure()

#     # Show the accuracy
#     plt.plot(x, accuracy, c=(1, 0, 0), label="Training Accuracy")
#     plt.plot(x, test_accuracy, c=(0, 0, 1), label="Test Accuracy")
#     plt.title('Accuracy')
#     plt.legend()
    
#     # Create a figure for the Loss
#     plt.figure()

#     plt.plot(x, loss, c=(1, 0, 0), label="Training Loss")
#     plt.plot(x, test_loss, c=(0, 0, 1), label="Training Loss")
#     plt.title('Loss')
#     plt.legend()
