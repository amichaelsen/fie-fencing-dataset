from progress.bar import Bar
import time 

bar = Bar('Processing', max=10)
for i in range(10):
    time.sleep(0.25)
    bar.next() 
bar.finish()

list1 = [1,2,3,4,5,6,7]

with Bar('Loading fencers', max=len(list1)) as bar:
    for l in list1:
        time.sleep(0.5)
        bar.next()
    bar.finish()        

for i in Bar('Loading tournaments').iter(range(20)):
    k = i*i
    time.sleep(0.15)