#include "opencv2/opencv.hpp"
#include <time.h>
#include <unistd.h>



using namespace cv;


RNG rng(12345);

int main(int, char**)
{
    VideoCapture cap(0); // open the default camera
    sleep(0.25);
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    int x = 0;
    int y = 0;
    

    int  numOfFrame = 100;
    int count = numOfFrame;
    
    Mat edges;
    Mat edges1;
    Mat canny_output;
    
    Mat firstFrame;
    Mat firstFrame1;


    Mat absdiff_output;
    vector<Vec4i> hierarchy;  
    vector<vector<Point> > contours;
    Mat thresh;  
    Mat dilate_output; 

    namedWindow("edges",1);


    for(;;)
    {
        Mat frame;
        cap >> frame; // get a new frame from camera  
        Mat resized;


         // # resize the frame, convert it to grayscale, and blur it

        resize(frame, frame, Size(500, 500));
        cvtColor(frame, edges, COLOR_BGR2GRAY);
        GaussianBlur(edges, edges1, Size(7,7),1.5,1.5, 0);
      //  Canny(edges1, canny_output, 0, 30, 3);

        //  # if the first frame is None, initialize it
        if( firstFrame.empty())
         {
            // reference by value 

            edges.copyTo(firstFrame) ;
             // firstFrame = edges;    
              continue;
         }

         //# compute the absolute difference between the current frame and
         //# first frame
        absdiff(firstFrame, edges1,absdiff_output  );
      //  imshow("firstFrame", firstFrame);
        threshold( absdiff_output, thresh, 50, 255,CV_THRESH_BINARY);
        //# dilate the thresholded image to fill in holes, then find contours
        //# on thresholded image
        dilate(thresh, dilate_output, Mat(), Point(-1, -1), 2, 1, 1);
        findContours( dilate_output, contours,  CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE );


  //    # loop over the contours
        //  

  vector<vector<Point> > contours_poly( contours.size() );
  vector<Rect> boundRect( contours.size() );
  for( size_t i = 0; i < contours.size(); i++ )
     { 


       approxPolyDP( Mat(contours[i]), contours_poly[i], 1, true );
       boundRect[i] = boundingRect( Mat(contours_poly[i]) );
      }
  
  for( size_t i = 0; i< contours.size(); i++ )
     {


            int x = boundRect[i].br().x;
            int y = boundRect[i].br().y;
            if( contourArea(Mat(contours_poly[i]) ) < 300)
             { 

             continue;



             }

             // std::cout << boundRect[i].tl()<< std::endl;
             // std::cout << boundRect[i].br()<< std::endl;

            if( (x > 50 )&& (y > 50 ) )
             {

            
            rectangle( frame, boundRect[i].tl(), boundRect[i].br(), cv::Scalar(0, 255, 0));

            }



     }


     count = count - 1;
     std::cout << count;

    if( count ==0)
     {
     
            edges.copyTo(firstFrame) ;
            count = numOfFrame;
     }



        // imshow("dilate_output", dilate_output);
        // imshow("absdiff_output", absdiff_output);
        // imshow("frame", frame);
        if(waitKey(30) >= 0) break;
    }
  return 0;
}
