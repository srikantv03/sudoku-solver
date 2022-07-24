# Sudoku-Solver

This is just a simple side-project which combines my recreational hobby of sudoku with my programming. This is an attempt to make an algorithm by myself, pooling little to no outside help and mapping the logic individually.

## Inner Workings

The core algorithm, located in the main.py file, is comprised of a series of "helper functions" (abstractions) and one large, recursive solve function. With the use of the abstractions, the recursive function uses the following workflow to determine a solution for the inputted sudoku puzzle.

![Sudoku Workflow Diagram](img/sudoku_diagram.png)

## API Details

The api interface for this algorithm is fairly simple to set up and use. The api uses tornado and listens on port 3000. To run the api, simply load all of the packages and run the main.py file on whatever interface you please. The gui will assume the api is running on localhost:3000, but if it is through a different IP, you are able to change that detail in the code!

## GUI Details

The gui for this application serves the purpose of calling the api in a non-programmatic way. The gui is set with a 9x9 sudoku grid in which the user is able to input the known values (sudoku clues) and send the puzzle to the api to solve. In some cases, the api is unable to solve the puzzle, and when this happens, the api will just send 0s for each square it is unable to find the number for.

The following is the layout of the gui:

![GUI Diagram](img/ui_ss.PNG)

## Visual Sudoku Solver

As an addition to the original algorithm, I have also worked on implementing ways for users to scan a sudoku puzzle and solve it using the algorithm and some computer vision.

The algorithm uses 4 steps to solve a sudoku board from the image

1. Using contour imaging, the algorithm looks for all quadrilateral (could be a sudoku board) contours, and chooses the largest one that is not directly adjacent to the border of the image

2. Since 9x9 sudoku boards are standard in having 81 squares, the algorithm is able to divide the sudoku board into 81 squares using a similar contour imaging process as in the first step

3. Using a trained model on the MNIST handwritten digits database, the algorithm uses a CNN to match the pixels in each cell of the sudoku board to a digit from 1-9, or a blank sudoku square

4. Finally, the algorithm sends this sudoku board to the API, and gets a response with the solution
