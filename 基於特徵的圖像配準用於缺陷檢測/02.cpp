int main(int argc, char **argv)
{
    // Read reference image
    string refFilename("8.jpg");
    cout <<"Reading reference image : "<< refFilename << endl;
    Mat imReference = imread(refFilename);

    // Read image to be aligned
    string imFilename("7.jpg");
    cout <<"Reading image to align : "<< imFilename << endl;
    Mat im = imread(imFilename);

    // Registered image will be resotred in imReg. 
    // The estimated homography will be stored in h. 
    Mat imReg, h;

    // Align images
    cout <<"Aligning images ..."<< endl;
    alignImages(im, imReference, imReg, h);

    // Write aligned image to disk. 
    string outFilename("aligned.jpg");
    cout <<"Saving aligned image : "<< outFilename << endl;
    imwrite(outFilename, imReg);

    // Print estimated homography
    cout <<"Estimated homography : \n"<< h << endl;
    Mat currentframe, previousframe;
    cvtColor(imReference, previousframe, COLOR_BGR2GRAY);
    cvtColor(imReg, currentframe, COLOR_BGR2GRAY);  //转化为单通道灰度图

    absdiff(currentframe, previousframe, currentframe);//做差求绝对值
    imshow("1", currentframe);
    imwrite("re.jpg", currentframe);
    threshold(currentframe, currentframe, 120, 255.0, THRESH_BINARY);
    imwrite("re11.jpg", currentframe);

    erode(currentframe, currentframe, Mat());//腐蚀
    dilate(currentframe, currentframe, Mat());//膨胀
    dilate(currentframe, currentframe, Mat());//膨胀

    imshow("moving area", currentframe);    //显示图像

    vector<vector<Point>> v;
    vector<Vec4i> hierarchy;
    Mat result;
    Rect rect;
    findContours(currentframe, v, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);
    for (int i = 0; i < hierarchy.size(); i++)
    {
        rect = boundingRect(v.at(i));
        if (rect.area() > 1)
        {
            rectangle(imReg, rect, Scalar(0, 0, 255), 2);
        }
    }

    imwrite("res1.jpg", imReg);
    imshow("moving area1", imReg);
    waitKey(0);
}