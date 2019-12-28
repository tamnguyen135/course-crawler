import scrapy
from scrapy.selector import Selector

class CourseSection:
	course = '' 
	section = ''
	empty_seats = 0

# Questions:
# what does yield return, and how does one extract things from yield?
# differences between get and extract?

# Tasks:
# organise the data extracted


main_url = 'https://courses.students.ubc.ca'

class CourseCrawl(scrapy.Spider):
	name = "course_crawler"
	start_urls = ['https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments']
	courses = []

	def parse(self, response):
		for subject_link in response.xpath('//tr[@class="section1"]/td/a/@href').getall():
			yield scrapy.Request(response.urljoin(main_url + subject_link),
                callback = self.parseSubject)

		for subject_link in response.xpath('//tr[@class="section2"]/td/a/@href').getall():
			yield scrapy.Request(response.urljoin(main_url + subject_link),
                callback = self.parseSubject)	

	def parseSubject(self, response):
		for course_link in response.xpath('//tr[@class="section1"]/td/a/@href').getall():
			yield scrapy.Request(response.urljoin(main_url + course_link), callback = self.parseCourse)

		for course_link in response.xpath('//tr[@class="section2"]/td/a/@href').getall():
			yield scrapy.Request(response.urljoin(main_url + course_link), callback = self.parseCourse)

	def parseCourse(self, response):
		for course_link in response.xpath('//tr[@class="section1"]/td[2]/a/@href').getall():
			yield scrapy.Request(response.urljoin(main_url + course_link), callback = self.parseSection)

		for course_link in response.xpath('//tr[@class="section2"]/td[2]/a/@href').getall():
			yield scrapy.Request(response.urljoin(main_url + course_link), callback = self.parseSection)


	def parseSection(self, response):
		yield {
			'subject': response.xpath('//ul[@class = "breadcrumb expand"]/li[3]/a/text()').extract_first(),
			'course': response.xpath('//ul[@class = "breadcrumb expand"]/li[4]/a/text()').extract_first(), 
			'section': response.xpath('//ul[@class = "breadcrumb expand"]/li[5]/text()').extract_first(), 
			'remaining seats': response.xpath('//tr[td[1]/text() = "Total Seats Remaining:"]/td[2]/strong/text()').extract_first()
		}




