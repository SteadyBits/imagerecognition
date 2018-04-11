import logging

from PIL import Image
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from IBMInterview import IBMHomework as IBM, settings

logger = logging.getLogger(__name__)

def landing(request):
    return render(request, 'payment/payment.html')

def home(request):
    templat = 'base.html'
    return render(request, 'dashboard.html', {'templat':templat})

@csrf_exempt
def upload_and_predict(request):

    if request.method == 'POST':
        image_data = request.POST.get('image')
        import re
        pattern = r'^data:(?P<mime_type>[^;]+);base64,(?P<image>.+)$'
        result = re.match(pattern, image_data)
        if result:

            mime_type = result.group('mime_type')
            print(mime_type)
            image = result.group('image').decode('base64')
            file = open(settings.STATIC_ROOT + 'images' + '.png', 'w')
            file.write(image)
        # folder_dataset_test = IBM.dset.ImageFolder(root=IBM.Config.testing_dir)
        # siamese_dataset = IBM.SiameseNetworkDataset(imageFolderDataset=folder_dataset_test,
        #                                         transform=IBM.transforms.Compose([IBM.transforms.Scale((100, 100)),
        #                                                                       IBM.transforms.ToTensor()
        #                                                                       ])
        #                                         , should_invert=False)
        #
        # test_dataloader = IBM.DataLoader(siamese_dataset, num_workers=6, batch_size=1, shuffle=True)
        # img_class = predict(test_dataloader)

    return render(request, 'dashboard.html', {'class': 1})


folder_dataset_test = IBM.dset.ImageFolder(root=IBM.Config.testing_dir)
siamese_dataset = IBM.SiameseNetworkDataset(imageFolderDataset=folder_dataset_test,
                                        transform=IBM.transforms.Compose([IBM.transforms.Scale((100, 100)),
                                                                      IBM.transforms.ToTensor()
                                                                      ])
                                        , should_invert=False)

train_dataloader = IBM.DataLoader(siamese_dataset, num_workers=6, batch_size=1, shuffle=True)

def predict(test_dataloader):

    dataiter = iter(test_dataloader)
    x0, _, _ = next(dataiter)

    for i in range(10):
        _, x1, label2 = next(dataiter)
        concatenated = IBM.torch.cat((x0, x1), 0)
        net = IBM.SiameseNetwork()
        net.load_state_dict(IBM.torch.load('image_model.pkl'))
        output1, output2 = net(IBM.Variable(x0).cuda(), IBM.Variable(x1).cuda())
        euclidean_distance = IBM.F.pairwise_distance(output1, output2)
        print(IBM.torchvision.utils.make_grid(concatenated))
        print('Dissimilarity: ', format(euclidean_distance.cpu().data.numpy()[0][0]))
    return 1