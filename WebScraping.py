import scrapy
import pandas as pd


class QuotesSpider(scrapy.Spider):
    name = "Job_Listing_for_Data_Analytics_position"

    def start_requests(self):
        urls = ['https://www.naukri.com/data-analyst-jobs-in-delhi-ncr']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        job_titles = response.xpath("//li[@class='desig']/@title").extract()
        all_jobs = list()
        for count, job in enumerate(response.css("div.row")):
            if count == 0:
                continue
            if len(job_titles) == 0:
                break
            all_jobs.append({
                'Job Title': job_titles.pop(0),
                'Experience Required':job.css("span.exp::text").extract_first(),
                'Location':job.xpath("//span[@class='loc']/span/text()").extract_first(),
                'Company Name': job.css('span.org::text').extract_first(),
                'Job Description Page':job.xpath("//a[@id='jdUrl']/@href").extract_first(),
                'Keyskills':job.css("span.skill::text").extract_first(),
                'Job Description':job.css("span.desc::text").extract_first(),
                'Salary':job.css("span.salary::text").extract_first()
            })

        df = pd.DataFrame(all_jobs)
        df.to_csv("naukri_dataanalytics.csv", sep=',')

