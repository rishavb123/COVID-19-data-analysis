@echo off
deldir data
git clone https://github.com/CSSEGISandData/COVID-19.git
rename COVID-19 data
cd data
deldir .git
cd ..
git add data
git commit -m "updated data from John Hopkins github repo"
git push