import org.opencv.core.*;
import org.opencv.highgui.HighGui;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.opencv.videoio.VideoCapture;

public class DetectarFotoEVideo {
    static{ System.loadLibrary(Core.NATIVE_LIBRARY_NAME); }

    public static void main(String[] args) {
        // Load the cascade
        CascadeClassifier faceDetector = new CascadeClassifier();
        faceDetector.load("haarcascade_frontalface_default.xml");

        // Read the input image
        Mat image = Imgcodecs.imread("test.jpg");

        // Convert into grayscale
        Mat grayImage = new Mat();
        Imgproc.cvtColor(image, grayImage, Imgproc.COLOR_BGR2GRAY);

        // Detect faces
        MatOfRect faceDetections = new MatOfRect();
        faceDetector.detectMultiScale(grayImage, faceDetections);

        // Draw rectangle around the faces
        for (Rect rect : faceDetections.toArray()) {
            Imgproc.rectangle(image, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height), new Scalar(0, 255, 0));
        }

        // Display the output
        HighGui.imshow("Image", image);
        HighGui.waitKey();

        // To capture video from webcam.
        VideoCapture cap = new VideoCapture(0);

        while (true) {
            // Read the frame
            if (!cap.read(image)) {
                System.out.println("Video camera is not working.");
                break;
            }

            // Convert into grayscale
            Imgproc.cvtColor(image, grayImage, Imgproc.COLOR_BGR2GRAY);

            // Detect faces
            faceDetections = new MatOfRect();
            faceDetector.detectMultiScale(grayImage, faceDetections);

            // Draw rectangle around the faces
            for (Rect rect : faceDetections.toArray()) {
                Imgproc.rectangle(image, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height), new Scalar(0, 255, 0));
            }

            // Display the output
            HighGui.imshow("Image", image);

            // Stop if escape key is pressed
            char c = (char) HighGui.waitKey(20);
            if (c == 27) {
                break;
            }
        }

        // Release the VideoCapture object
        cap.release();
    }
}
