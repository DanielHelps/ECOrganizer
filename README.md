![2022-07-06_11-23-08-550](https://user-images.githubusercontent.com/101622750/177505194-e6c192b7-5835-4268-83fd-13d61ac59ce6.jpg)


# ECOrganizer
An app that performs various checks to manufacturing and assembly drawings based on “Kornit Digital” drawing template.

## ECOrganizer main GUI
![ECOrganizer main GUI](https://user-images.githubusercontent.com/101622750/177507465-b5fff2c5-7322-4727-b0f9-8fb9e12bdba2.png)

The app can accept either a folder or a selection of files.

The user can decide what checks to perform, and after the checks are performed, a log of issues can be exported to excel.

## The avaliable checks

### Drawing nuber check
![drawing_number_comp](https://user-images.githubusercontent.com/101622750/177507484-268a8124-6ce2-4f7d-9ceb-611cd4f9a5e2.png)

Checks that the drawing number in the PDF and the name of the file are the same.

### Part numbers check
![pn_check](https://user-images.githubusercontent.com/101622750/177507491-63cff978-d4e2-4f29-af10-f73f9bdf3a13.png)

Checks that the P/N of the drawing is a valid Kornit P/N.

### Drawing revisions check
![rev_comp](https://user-images.githubusercontent.com/101622750/177507503-5d3ea7a1-0f42-4ede-851d-d0dd0d2148b1.png)

Checks that the revision in the PDF is the same as the revision in the file name.

### Signature check
![signs_check](https://user-images.githubusercontent.com/101622750/177507511-52c35921-b61b-48fb-b876-cc00d695a1d2.png)

Checks that all the required signatures are present.

### Balloons check
![baloons_check](https://user-images.githubusercontent.com/101622750/177507520-c5da46c8-b0a8-4b85-8a2e-38e49ac8399c.png)

Verifies that the exact required balloons are present (for example, if there is an assembly with 12 items, so balloons with all the 12 items should be present).

### Date check
![date_check](https://user-images.githubusercontent.com/101622750/177507531-9445e893-30d2-407e-b34c-aebe0c883be3.png)

Checks that a date exists in the drawing.


## Log
The log for an example folder can be seen below:

![ECOrganizer log](https://user-images.githubusercontent.com/101622750/177512361-c5826c52-d5ee-4bc5-95ce-2e5a4a336d5a.png)

The log can be exported to excel by pressing the "Export to excel" button.

## Run the repository
In order to run the app, clone the repo and run file ```ECOrgaznier.py``` or use the following command to create an exectuable:

```pyinstaller --onefile --windowed --icon icon.ico ECOrganizer.py```
