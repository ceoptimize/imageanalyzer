
from gptimageanalyzer import GPTImageAnalyzer


if __name__ == '__main__':

    analyzer = GPTImageAnalyzer()
    # To analyze multiple images from a folder
    analyzer.analyze_multiple_images(
        image_folder='images', 
        prompt='This image contains a sign-in sheet for a bootcamp. Please extract all the data except signatures into a csv format. You can use the other images to cross-reference names if they are not clear in the sign-in sheet. If the name matches I have a preference for the longer/fuller name, wherever the source.', 
        output_folder='output/text_results', 
        output_file='output_multiple.txt'
    )
    # To analyze a single image
    analyzer.analyze_single_image(
        image_path='images/facebook1.jpeg', 
        prompt='Summarize this image', 
        output_folder='output/text_results', 
        output_file='single_output.txt'
    )
