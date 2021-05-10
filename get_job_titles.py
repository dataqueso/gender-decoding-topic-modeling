"""
Top job titles found in export of data from the U.S. Bureau of Labor
Statics website for Labor Force Statistics from the Current Population Survey.
Source:  https://www.bls.gov/cps/cpsaat11.htm

"""
import pandas as pd
import copy

def get_titles_by_gender(csv_file, threshold):
    """
    Read csv file and output the job titles
    by gender
    """
    data = pd.read_csv(csv_file, header=1)
    print(data.head())
    print(data.shape)
    
    data['Occupation'] = pd.Series([str(d) for d in data['Occupation']])
    data = data[~data.Occupation.str.contains("nan")]
    data = data[~data.Occupation.str.contains("occupations")]
    data.index = range(data.shape[0])

    data = data.sort_values(by='Women', ascending=False)

    list_female_titles = []
    list_male_titles = []
    female_percents = []
    male_percents = []
    for i in range(data.shape[0]):
        percent_women = data.loc[i,'Women']
        occupation = data.loc[i,'Occupation']
        try:
            percent_women = float(percent_women)/100.0
            if percent_women >= threshold:
                list_female_titles.append(occupation)
                female_percents.append(percent_women)
            if percent_women <= 1-threshold:
                list_male_titles.append(occupation)
                male_percents.append(percent_women)
        except ValueError as exp:
            pass

    female_df = pd.DataFrame(list_female_titles, columns=['Occupation'])
    female_df['Percentage'] = female_percents
    male_df = pd.DataFrame(list_male_titles, columns=['Occupation'])
    male_df['Percentage'] = male_percents

    female_df = female_df.sort_values(by='Percentage', ascending=False)
    male_df = male_df.sort_values(by='Percentage', ascending=True)

    print('Female occupations ', female_df.head(10))
    print('Male occupations ', male_df.head(10))

    female_df.head(50).to_csv("data/female_occupations_top.csv", index=False)
    male_df.head(50).to_csv("data/male_occupations_top.csv", index=False)


def main():
    """Main driver func"""

    # Use threshold*100 % as cutoff for percent women/men in a job title
    get_titles_by_gender('us_bureau_labor_stats_occupations.csv', threshold=0.7)

if __name__ == '__main__':
    main()
