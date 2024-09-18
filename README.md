# TaxCalculator
A tax program written for **PMS** and **THE DOG WAGGIN**. Essentially summarizes all costs into specific categories into a readable format. There are three primary methods in how you can use this program, either manual creation of the inital document or 2 other methods of using chase CSV statements. 
## How to Run the Program
If you already have an existing document all you need to do is run:
```
python3 main.py {path to formatted document}
```
If **csv** files are provided all you need to do is run:
```
python3 main.py
```
## Getting Started
1. Create a manual document using this formating technique. 
```
"Name(No duplicates allowed and fully numeric names not allowed)"
For the numeric section under the following formats are acceptable. 


100, 200, 300, 400


or 


100


200


300.05


or


100 200 300


or 


$100 $200 $300
```

Example:

```
Gas


100 200 56.40 39.59
```
2. Go to the chase website, login and download a **csv** file format of your credit card statement for the previous year. Then put this in the **resources** folder. Pick all the categories and enter them based on the statements. If duplicate statements exist they are input into the same category. 

3. Go to the chase website, login and download a checking account statement as a **csv** for the previous year and put it in the **resources** folder. Pick all categories to put the statements in. 
## What is Returned
With the gas example it would give you the line:
```
Gas: $395.99
```
The program will also ask you to name a new document which will give you a **txt** document with the summarized categories. 
## Future Plans
- [ ] Create a UI to use rather than using terminal for taxes
- [ ] Creating a better way to recognize similar statements rather than using regex
- [ ] Give the user the option to create a latex PDF document based on the finalized data
- [ ] Create an intermediate saving feature so you do not need to do everything in one go 
- [ ] Better error handling