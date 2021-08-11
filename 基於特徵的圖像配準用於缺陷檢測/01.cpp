constint MAX_FEATURES = 5000;
constfloat GOOD_MATCH_PERCENT = 0.45f;
//im1为待配准图片
//im2为模板图片
//im1Reg为配准后的图片
//h为单应性矩阵
void alignImages(Mat&im1, Mat&im2, Mat&im1Reg, Mat&h)
{
    // 将图像转为灰度图
    Mat im1Gray, im2Gray;
    cvtColor(im1, im1Gray, COLOR_BGR2GRAY);
    cvtColor(im2, im2Gray, COLOR_BGR2GRAY);

    // 存储特征与特征描述子的变量
    std::vector<KeyPoint> keypoints1, keypoints2;
    Mat descriptors1, descriptors2;

    // 检测ORB特征计算特征描述子.
    Ptr<Feature2D> orb = ORB::create(MAX_FEATURES);
    orb->detectAndCompute(im1Gray, Mat(), keypoints1, descriptors1);
    clock_t start, end;
    start = clock();
    orb->detectAndCompute(im2Gray, Mat(), keypoints2, descriptors2);  //77ms

    // 特征匹配.
    std::vector<DMatch> matches;
    Ptr<DescriptorMatcher> matcher = DescriptorMatcher::create("BruteForce-Hamming");
    matcher->match(descriptors1, descriptors2, matches, Mat());
    // Sort matches by score
    std::sort(matches.begin(), matches.end());

    //基于GMS的特征匹配算法
    //vector<DMatch> matchesAll, matchesGMS;
    //BFMatcher matcher(NORM_HAMMING);
    //std::vector<DMatch> matches;
    //matcher.match(descriptors1, descriptors2, matchesAll);
    //cout << "matchesAll: " << matchesAll.size() << endl;
    //matchGMS(im1.size(), im2.size(), keypoints1, keypoints2, matchesAll, matches);
    //std::sort(matches.begin(), matches.end());

    end = clock();
    cout << (float)(end - start) * 1000 / CLOCKS_PER_SEC<<"ms"<< endl;

    // 移除不好的匹配点
    constint numGoodMatches = matches.size() * GOOD_MATCH_PERCENT;
    matches.erase(matches.begin() + numGoodMatches, matches.end());
    // 画匹配点
    Mat imMatches;
    drawMatches(im1, keypoints1, im2, keypoints2, matches, imMatches);
    imwrite("matches.jpg", imMatches);

    // 存储好的匹配点
    std::vector<Point2f> points1, points2;

    for (size_t i = 0; i < matches.size(); i++)
    {
        points1.push_back(keypoints1[matches[i].queryIdx].pt);
        points2.push_back(keypoints2[matches[i].trainIdx].pt);
    }

    // 找出最优单映射变换矩阵h
    h= findHomography(points1, points2, RANSAC);

    // 利用h矩阵进行透视变换
    warpPerspective(im1, im1Reg, h, im2.size());
}