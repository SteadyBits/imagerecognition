import base64

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from IBMInterview import IBMHomework as IBM, settings
from django.http.response import JsonResponse

def home(request):
    templat = 'base.html'
    return render(request, 'dashboard.html', {'templat':templat})

def predict(test_dataloader):
    dataiter = iter(test_dataloader)
    x0, x1, label2 = next(dataiter)
    concatenated = IBM.torch.cat((x0, x1), 0)
    net = IBM.SiameseNetwork()
    net.load_state_dict(IBM.torch.load(settings.STATIC_ROOT + '/image_model.pkl'))
    output1, output2 = net(IBM.Variable(x0).cpu(), IBM.Variable(x1).cpu())
    euclidean_distance = IBM.F.pairwise_distance(output1, output2)
    if (euclidean_distance.cpu().data.numpy()[0][0]) > 0.5:
        return 1
    else:
        return 2

@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        f = (request.FILES.get('image'))
        if f is None:
            import re
            imgstr = request.POST.get('image')
            imgstr = re.search(r'base64,(.*)', imgstr).group(1)
            output = open(settings.STATIC_ROOT + '/test_dir/faces/test.png', 'wb+')
            imgstr = base64.b64decode(imgstr)
            output.write(imgstr)
            output.close()
        else:
            destination = open(settings.STATIC_ROOT + '/test_dir/faces/test.png', 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        folder_dataset_test = IBM.dset.ImageFolder(root=IBM.Config.test_dir)
        siamese_dataset = IBM.SiameseNetworkDataset(imageFolderDataset=folder_dataset_test,
                                                    transform=IBM.transforms.Compose([IBM.transforms.Scale((100, 100)),
                                                                                      IBM.transforms.ToTensor()
                                                                                      ])
                                                    , should_invert=False)

        test_dataloader = IBM.DataLoader(siamese_dataset, num_workers=6, batch_size=1, shuffle=False)

        status = predict(test_dataloader)
        templat = 'base.html'
    return render(request, 'dashboard.html', {'templat': templat, 'imgclass': status} )

@csrf_exempt
def file_upload_api(request):
    if request.method == 'POST':
        f = (request.FILES.get('image'))
        if f is None:
            import re
            imgstr = request.POST.get('image')
            imgstr = re.search(r'base64,(.*)', imgstr).group(1)
            output = open(settings.STATIC_ROOT + '/test_dir/faces/test.png', 'wb+')
            imgstr = base64.b64decode(imgstr)
            output.write(imgstr)
            output.close()
        else:
            destination = open(settings.STATIC_ROOT + '/test_dir/faces/test.png', 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        folder_dataset_test = IBM.dset.ImageFolder(root=IBM.Config.test_dir)
        siamese_dataset = IBM.SiameseNetworkDataset(imageFolderDataset=folder_dataset_test,
                                                    transform=IBM.transforms.Compose([IBM.transforms.Scale((100, 100)),
                                                                                      IBM.transforms.ToTensor()
                                                                                      ])
                                                    , should_invert=False)

        test_dataloader = IBM.DataLoader(siamese_dataset, num_workers=6, batch_size=1, shuffle=False)
        status = predict(test_dataloader)

    return JsonResponse({'object_class': status})
