# Booth Course Planner

A course planner for the Booth School of Business. The planner merges the following variables into one place.

1. Course schedule
1. Degree and concentration requirements
1. Bid prices and seat availability
1. Course evaluations

## Installation

Clone the repository

```bash
git clone https://github.com/ssordopalacios/booth-course-planner
```

Set up the anaconda environment

```bash
conda env create --prefix ./env -f environment.yml
```

Download the data files from the intranet

* Booth Schedule
  * Click [link](https://intranet.chicagobooth.edu/secure/evewkd/coursesearch/coursesearch)
  * Select *Search Course Schedule (spreadsheet)*
  * Select *Download to Excel*
  * Save as `data/BoothSchedule.xlsx`
* Requirements
  * Degree Requirements
    * Click [link](https://intranet.chicagobooth.edu/secure/evewkd/academics/cdr/course-related-information/degree-requirements)
    * Manually clean each into `Area: Course, Course`
    * Save as `data/degree_requirements.txt`
  * Concentration requirements
    * Click [link](https://intranet.chicagobooth.edu/secure/evewkd/academics/cdr/course-related-information/concentration-requirements)
    * Manually clean each into `Area: Course, Course`
    * Save as `data/concentration_requirements.txt`
* Price History
  * Click [link](https://ibid.chicagobooth.edu/registrar-student/Home.tap)
  * Select *Course Price History*
  * Save as `data/course price history.xls`
* Course Evaluations
  * Click [link](https://intranet.chicagobooth.edu/pub/coursesearch/CourseEvaluation)
  * Historical
    * Select *Full-time, Evening, Weekend and PhD Course Evaluations*
    * Select *Download Course Evaluation Results (Data Only in Excel format)*
    * Save as `data/course_evals.xlsx`
  * New MBA
    * Select *Winter 2020- Spring 2021 MBA Evaluations (Excel)*
    * Select *To view the Chicago Booth Evaluations Results, please click here*
    * Save as `data/ExportReport_MBA.csv`

## Usage

Activate the anaconda environment

```bash
conda activate ./env
```

Create the course planning overview

```bash
python main.py
```

The overview is created with the following procedure:

1. Read and clean the course schedule
1. Generate degree and concentration requirements that each `Course` satisfies
1. Merge requirements into schedule by `Course`
1. Read and clean the price history
1. For each `Course`-`Quarter`-`Program` combination, calculate median price history
1. Merge price history into schedule by `Course`-`Quarter`-`Program`
1. Read and clean the course evaluations
1. For each `Course`-`Last Name` combination, calculate median course evaluations
1. Merge course evaluations by `Course`-`Last Name`
1. Save the file to `output/booth_course_planner.csv`

## Contributing

Open an issue on [GitHub](https://github.com/ssordopalacios/booth-course-planner/issues)

Updating anaconda environment with new LOCAL dependencies

```bash
conda env export > environment.yml
```

Update anaconda environment with new REMOTE dependencies

```bash
conda env update --prefix ./env --file environment.yml  --prune
```

## Authors

* Santiago I. Sordo Palacios
