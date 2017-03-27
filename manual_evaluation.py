import shuffle_all as shuffler
import solr, os.path
import classifier_exact_match as auto_matcher

# CONFIGURATION

# A list containing four elements:
# [0] a label for the links evaluation
# [1] the folder containing the original links to shuffle first
# [2] the folder containing the links to annotate
# [3] the name of the file containing the links
annotation_pair = ["Exact match links","/home/paolo/python_code/links/solr/classifier_exact_match/", "/home/paolo/python_code/links/solr/classifier_exact_match-shuffled/","links_to_evaluate.csv"]
annotation_pair = ["Double classification links","/home/paolo/python_code/links/new/950/original/", "/home/paolo/python_code/links/new/950/shuffled/","links.csv"]
annotation_pair = ["Double classification links","/home/paolo/python_code/links/new/Homefix/original/", "/home/paolo/python_code/links/new/Homefix/","links.csv"]


# the folder containing the links to annotate
#links_folder = "/home/paolo/python_code/links/solr/classifier_exact_match-shuffled/"
#links_folder = "/home/paolo/python_code/links/sample_random/shuffled-annotation/"
#links_folder = "/home/paolo/python_code/links/new/950/shuffled/"

# the folder containing the original links to shuffle first
#shuffle_source_dir = "/home/paolo/python_code/links/solr/classifier_exact_match/"
#shuffle_source_dir = "/home/paolo/python_code/links/sample_random/original/"
#shuffle_source_dir = "/home/paolo/python_code/links/new/950/original/"


#target_name_param = "links_to_evaluate.csv"
#target_name_param = "950_0result_links.txt"

annotation_aid = True

# CONFIGURATION END
links_folder = annotation_pair[2]
shuffle_source_dir = annotation_pair[1]
target_name_param = annotation_pair[3]
def ask_similarity(uri1, uri2):
  print "###############################################################"
  print uri1
  print solr.get_label(uri1)
  print "\n"
  print uri2
  print solr.get_label(uri2)
  print "\n\n"
  if annotation_aid:
    if auto_matcher.classify(solr.get_label(uri1),solr.get_label(uri2)):
      print " --- !!! WARNING !!! POTENTIAL MATCH DETECTED !!! ---"
    similar_words = auto_matcher.count_similar_words(solr.get_label(uri1),solr.get_label(uri2))
    s_w_string = "("+str(similar_words)+")"
    while similar_words > 0:
      similar_words -=1
      s_w_string = s_w_string+" <(SW)> "
    print s_w_string+"\n"
  print "Type:\np (positive) q (negative) s (skip) e (end)"
  input = raw_input("--> ")
  if input == "p":
    return "pos"
  if input == "q":
    return "neg"
  if input == "s":
    return "skip"
  if input == "e":
    return "end"
  return ""

def log_decision(log_file,s,t,similarity):
  log_file.write("<" + s + "> " + solr.get_label(s) + "\n")
  log_file.write("<" + t + "> " + solr.get_label(t) + "\n")
  log_file.write(similarity+"\n\n")

def print_status(ann,pos,neg,skip):
  print "* " + str(ann) + " " + str(pos) + " " + str(neg) + " " + str(skip)

def save_status(ann,pos,neg,skip):
  config_file = open(links_folder + "config.csv", 'a')
  config_file.write("\n"+str(ann)+" "+str(pos)+" "+str(neg)+" "+str(skip))
  config_file.close()

def terminate(ann,pos,neg,skip):
  save_status(ann,pos,neg,skip)
  print "Annotation session terminated. "+str(ann)+" "+str(pos)+" "+str(neg)+" "+str(skip)

# Shuffle all the datapoints and create annotation metadata (e.g. nuber of datapoints annotated)
shuffle_dirs = [ [shuffle_source_dir, links_folder]]

# initialise if necessary
if not (os.path.isfile(links_folder + target_name_param)):
  print "\n Shuffling data in directories: " + str(shuffle_dirs)
  shuffler.shuffle_all(shuffle_dirs, target_name_param)
  config_file = open(links_folder+"config.csv", 'w')
  config_file.write("0 0 0 0")
  config_file.close()
  print "Shuffling initialisation finished.\n"

# start annotation
annotated = -1
pos = -1
neg = -1
skipped = -1
skipped_new = -1
config_file = open(links_folder + "config.csv", 'r')
# TODO should just jump to last line
for line in config_file:
  if len(line) > 4:
    conf = line.split()
    annotated = int(conf[0])
    pos = int(conf[1])
    neg = int(conf[2])
    skipped_new = int(conf[3])
if annotated < 0 or pos < 0 or neg < 0 or skipped_new < 0:
  print "ERROR, configuration file empty or not correctly configured"
else:
  print "Annotation session started. " + str(annotated) + " " + str(pos) + " " + str(neg) + " " + str(skipped_new)
  skipped = annotated
  config_file.close()
  links_file = open(links_folder + target_name_param, 'r')
  for line in links_file:
    pos_file = open(links_folder + "r_pos.csv", 'a')
    neg_file = open(links_folder + "r_neg.csv", 'a')
    skipped_file = open(links_folder + "r_skipped.csv", 'a')
    log_file = open(links_folder + "r_log.csv", 'a')
    if skipped <= 0:
      pair = line.split()
      similarity = ""
      while similarity != "end" and similarity != "pos" and similarity != "neg" and similarity != "skip":
        print_status(annotated, pos, neg, skipped_new)
        similarity = ask_similarity(pair[0], pair[1])
      if similarity == "end":
        terminate(annotated,pos,neg,skipped_new)
        break
      else:
        log_decision(log_file,pair[0],pair[1],similarity)
      if similarity == "pos":
        pos_file.write(pair[0]+" "+pair[1]+"\n")
        pos += 1
        annotated += 1
      if similarity == "neg":
        neg_file.write(pair[0] + " " + pair[1] + "\n")
        neg += 1
        annotated += 1
      if similarity == "skip":
        skipped_file.write(pair[0] + " " + pair[1] + "\n")
        skipped_new += 1
        annotated += 1
      save_status(annotated, pos, neg, skipped_new)
    else:
      skipped -= 1
    pos_file.close()
    neg_file.close()
    skipped_file.close()
    log_file.close()
  links_file.close()
  terminate(annotated, pos, neg, skipped_new)


print "\n END \n"
