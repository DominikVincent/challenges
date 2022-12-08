import cv2
import io

import requests
import numpy as np
from PIL import Image
import re

# def get_image():
#     r = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/RichterJP.jpg/250px-RichterJP.jpg", headers={'User-Agent' : "Magic Browser"})
#
#     print("Request: ", r)
#     print("Content: ", r.content)
#
#     bytes_im = io.BytesIO(r.content)
#
#     img = Image.open(bytes_im)
#
#     img_np = np.array(img)
#     print(img_np.shape)
#     cv_im = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
#
#     print(cv_im)
#
#     import matplotlib.pyplot as plt
#
#     plt.imshow(cv_im)
#     plt.show()
#
# l = re.findall(r'/\d+px-', "http://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/RichterJP.jpg/250px-RichterJP.jpg")
# print(l)


# print(re.findall(r'.*?/\d+px-(.*)', "http://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Cat_flap.jpg/220px-Cat_flap.jpg"))
test_text = \
"""{{Short description|German Romantic writer}}
{{About||the West Indian cricketer|Jean Paul (cricketer)|other people of the same name|Jean-Paul (disambiguation){{!}}Jean-Paul}}

{{Use dmy dates|date=July 2014}}
{{Infobox writer <!-- for more information see [[:Template:Infobox writer/doc]] -->
| name = Johann Paul Friedrich Richter
| image = RichterJP.jpg
| imagesize = 250px
| caption = Portrait of Jean Paul by Heinrich Pfenninger (1798) 
| pseudonym = Jean Paul
| birth_name = Johann Paul Friedrich Richter
| birth_date = {{birth date|df=yes|1763|3|21}}
| birth_place = [[Wunsiedel]], [[Holy Roman Empire]]
| death_date = {{death date and age|df=yes|1825|11|14|1763|3|21}}
| death_place = [[Bayreuth]], [[German Confederation]]
| alma_mater = [[University of Leipzig]]
| occupation = Novelist
| nationality = German
| period = 1783–1825
| genre = Humorous novels and stories
| subject = Education, politics[[File:Jean Paul – Titan vol 1 – BEIC 3988100.jpg|thumb|''Titan. 1'']]
| movement = [[Romanticism]]
| awards = [[PhD (Hon)]]:<br/>[[University of Heidelberg]] (1817)
| signature =
}}

'''Jean Paul''' ({{IPA-de|ʒɑ̃ paʊl|lang|De-Jean Paul.ogg}};  born '''Johann Paul Friedrich Richter''', 21 March 1763 – 14 November 1825) was a [[German Romanticism|German Romantic]] writer, best known for his humorous novels and stories.

==Life and work==
Jean Paul was born at [[Wunsiedel]], in the [[Fichtelgebirge]] mountains ([[Franconia]]). His father was an organist at Wunsiedel. In 1765 his father became a pastor at [[Joditz]] near [[Hof, Germany|Hof]] and, in 1767 at [[Schwarzenbach an der Saale|Schwarzenbach]], but he died on 25 April 1779,{{sfn|Chisholm|1911}} leaving the family in great poverty.{{citation needed|date=June 2012}} Later in life, Jean Paul noted, "The words that a father speaks to his children in the privacy of home are not heard by the world, but as in [[Whispering gallery|whispering-galleries]], they are clearly heard at the end and by posterity."<ref>{{Cite book|url=https://books.google.com/books?id=fcYZlz0ezQUC&pg=PA389|title=The Child and Childhood in Folk Thought: (The Child in Primitive Culture), p. 389|last=Chamberlain|first=Alexander|date=1896|publisher=MacMillan|language=en}}</ref> After attending the ''Gymnasium'' at Hof, in 1781 Jean Paul went to the [[University of Leipzig]]. His original intention was to enter his father's profession, but theology did not interest him, and he soon devoted himself wholly to the study of literature. Unable to maintain himself at Leipzig he returned in 1784 to Hof, where he lived with his mother. From 1787 to 1789, he served as a tutor at [[Töpen]], a village near Hof; and from 1790 to 1794, he taught the children of several families in a school he had founded in nearby [[Schwarzenbach an der Saale|Schwarzenbach]].{{sfn|Chisholm|1911}}

Jean Paul began his career as a man of letters with ''Grönländische Prozesse'' ("[[Greenland]] Lawsuits"), published anonymously in Berlin in 1783–84, and ''Auswahl aus des Teufels Papieren'' ("Selections from the Devil's Papers", signed J. P. F. Hasus), published in 1789. These works were not received with much favour, and in later life even their author had little sympathy for their satirical tone.

Jean Paul's outlook was profoundly altered by a spiritual crisis he suffered on 15 November 1790, in which he had a vision of his own death. His next book, ''Die unsichtbare Loge'' ("The Invisible Lodge"), a romance published in 1793 under the pen-name Jean Paul (in honour of [[Jean-Jacques Rousseau]]), had all the qualities that were soon to make him famous, and its power was immediately recognized by some of the best critics of the day.{{sfn|Chisholm|1911}}

Encouraged by the reception of ''Die unsichtbare Loge'', Richter composed a number of books in rapid succession: ''Leben des vergnügten Schulmeisterleins Maria Wutz in Auenthal'' ("Life of the Cheerful Schoolmaster Maria Wutz", 1793), the best-selling ''Hesperus'' (1795), which made him famous, ''Biographische Belustigungen unter der Gehirnschale einer Riesin'' ("Biographical Recreations under the Brainpan of a Giantess", 1796), ''Leben des Quintus Fixlein'' ("Life of Quintus Fixlein", 1796), ''Der Jubelsenior'' ("The Parson in Jubilee", 1797), and ''Das Kampaner Tal'' ("The Valley of Campan", 1797). Also among these was the novel ''[[Siebenkäs]]'' in 1796–97.

''[[Siebenkäs]]''' slightly [[supernatural]] theme, involving a [[Doppelgänger]] and [[pseudocide]], stirred some controversy over its interpretation of the [[Resurrection]], but these criticisms served only to draw awareness to the author. This series of writings assured Richter a place in German literature, and during the rest of his life every work he produced was welcomed by a wide circle of admirers.

After his mother's death in 1797, Richter went to [[Leipzig]], and in the following year, to [[Weimar]],{{sfn|Chisholm|1911}} where he started work on his most ambitious novel, ''[[Titan (Jean Paul novel)|Titan]]'', published between 1800 and 1803.{{sfn|Chisholm|1911}} Richter became friends with such Weimar notables as [[Johann Gottfried Herder]], by whom he was warmly appreciated, but despite their close proximity, Richter never became close to [[Johann Wolfgang von Goethe]] or [[Friedrich Schiller]], both of whom found his literary methods repugnant; but in Weimar, as elsewhere, his remarkable conversational powers and his genial manners made him a favorite in general society.{{sfn|Chisholm|1911}} The British writers [[Thomas Carlyle]] and [[Thomas De Quincey]] took an interest in Jean Paul's work.{{sfn|Americana staff|1920}}<ref>{{Cite journal|last=Hindley|first=Meredith|date=2009|title=The Voracious Pen of Thomas Carlyle|journal=Humanities|volume=30|pages=228–230}}</ref>

[[File:Jean-Paul-Denkmal (02).jpg|thumb|The Jean Paul monument in Bayreuth, created by [[Ludwig Michael Schwanthaler|Ludwig von Schwanthaler]] and unveiled in 1841 on the 16th anniversary of Richter's death]]
In 1801, he married Caroline Meyer, whom he had met in Berlin the year before. They lived first at [[Meiningen]], then at [[Coburg]]; and finally, in 1804, they settled at [[Bayreuth]]. Here Richter spent a quiet, simple, and happy life, constantly occupied with his work as a writer. In 1808 he was delivered from anxiety about outward necessities by Prince Primate [[Karl Theodor Anton Maria von Dalberg|Karl Theodor von Dalberg]], who gave him an annual pension of 1,000 florins,{{sfn|Chisholm|1911}} which was later continued by the king of Bavaria.{{sfn|Americana staff|1920}}

Jean Paul's ''Titan'' was followed by ''Flegeljahre'' ("The Awkward Age", 1804–5).{{sfn|Chisholm|1911}} His later imaginative works were ''Dr Katzenbergers Badereise'' ("Dr Katzenberger's Trip to the Medicinal Springs", 1809), ''Des Feldpredigers Schmelzle Reise nach Flätz'' ("Army Chaplain Schmelzle's Voyage to Flätz", 1809), ''Leben Fibels'' ("Life of Fibel", 1812), and ''Der Komet, oder Nikolaus Marggraf'' ("The Comet, or, Nikolaus Markgraf", 1820–22). In ''Vorschule der Aesthetik'' ("Introduction to Aesthetics", 1804) he expounded his ideas on art; he discussed the principles of education in ''Levana, oder Erziehungslehre'' ("Levana, or, Pedagogy", 1807); and the opinions suggested by current events he set forth in ''Friedenspredigt'' ("Peace Sermon", 1808), ''Dämmerungen für Deutschland'' ("Twilights for Germany", 1809), ''Mars und Phöbus Thronwechsel im Jahre 1814'' ("Mars and Phoebus Exchange Thrones in the Year 1814", 1814), and ''Politische Fastenpredigten'' ("Political Lenten Sermons", 1817). In his last years he began ''Wahrheit aus Jean Pauls Leben'' ("The Truth from Jean Paul's Life"), to which additions from his papers and other sources were made after his death by C. Otto and E. Förster.{{sfn|Chisholm|1911}}
[[File:Jean-Paul-Denkmal (02).jpg|thumb|The Jean Paul monument in Bayreuth, created by [[Ludwig Michael Schwanthaler|Ludwig von Schwanthaler]] and unveiled in 1841 on the 16th anniversary of Richter's death]]

Also during this time he supported the younger writer [[E. T. A. Hoffmann]], who long counted Richter among his influences. Richter wrote the preface to ''Fantasy Pieces'', a collection of Hoffmann's short stories published in 1814.{{citation needed|date=June 2012}}

In September 1821 Jean Paul lost his only son, Max, a youth of the highest promise; and he never quite recovered from this shock.{{sfn|Chisholm|1911}} He lost his sight in 1824,{{citation needed|date=June 2012}} and died of [[edema|dropsy]] at Bayreuth, on 14 November 1825.{{sfn|Chisholm|1911}}

==Characteristics of his work==
Jean Paul occupies an unusual position in German literature and has always divided the literary public. Some hold him in highest veneration while others treat his work with indifference. He took the Romantic formlessness of the novel to extremes: [[August Wilhelm Schlegel|Schlegel]] called his novels soliloquies, in which he makes his readers take part (in this respect going even further than [[Laurence Sterne]] in ''[[Tristram Shandy]]''). Jean Paul habitually played with a multitude of droll and bizarre ideas: his work is characterized by wild metaphors as well as by digressive and partly labyrinthine plots. He mixed contemplation with [[literary theory]]: alongside spirited irony the reader finds bitter [[satire]] and mild humour; next to soberly realistic passages there are romanticized and often ironically-curtailed [[idyll]]s, [[social commentary]] and political statements.  The quick changes of mood attracted the composer Schumann whose ''[[Papillons]]'' was inspired by Jean Paul.<ref>Explicating Jean Paul: Robert Schumann's Program for "Papillons," Op. 2 Eric Frederick Jensen ''[[19th-Century Music]]'', Vol. 22, No. 2 (Autumn, 1998), pp. 127-143 Published by: [[University of California Press]].  Accessed via JSTOR (subscription required). Article DOI: 10.2307/746854 Article Stable URL: https://www.jstor.org/stable/746854</ref>

His novels were especially admired by women. This was due to the empathy with which Jean Paul created the female characters in his works: never before in German literature were women represented with such psychological depth. At the same time however, his work contains misogynistic quips. Jean Paul's character may have been as diverse and as confusing as many of his novels: he was said to be very sociable and witty, while at the same time extremely sentimental: having an almost childlike nature, quickly moved to tears. It is obvious from his works that his interests encompassed not only literature but also astronomy and other sciences.

It is no surprise that the relationship of so capricious an author with the Weimar classicists [[Goethe]] and [[Schiller]] always remained ambivalent: Schiller once remarked that Jean Paul was as alien to him as someone who fell from the moon, and that he might have been worthy of admiration "if he had made as good use of his riches as other men made of their poverty."{{sfn|Chisholm|1911}} [[Johann Gottfried Herder|Herder]] and [[Christoph Martin Wieland|Wieland]] on the other hand fully appreciated his work and supported him. Although he always kept his distance from the classicists, who wanted to "absolutize" art, and although his theoretical approach (most notably in his ''Introduction to Aesthetics'') was considerably influenced by Romanticism, it would be misleading to call him a Romantic without qualification. Here too he kept his distance: with all his subjectivism he didn't absolutize the subject of the author as the Romantics often did. Jean Paul had what had become rare amidst classical severity and romantic irony: humour. He also was one of the first who approached humour from a theoretical standpoint.

He thought that both the [[Age of Enlightenment|Enlightenment]] and [[metaphysics]] had failed, though they still held importance for his worldview. He arrived at a philosophy without illusions, and a state of humorous resignation. Correspondingly he was one of the first defenders of [[Schopenhauer]]'s philosophy. He didn't try to indoctrinate but to portray human happiness, even (and especially) in an increasingly alienated environment — the rococo castles and bleak villages of Upper Franconia. Jean Paul was not only the first to use and name the literary motif of the [[Doppelgänger]], he also utilised it in countless variations (e.g. Siebenkäs and Leibgeber, Liane and Idoine, Roquairol and Albano). In his novel ''Siebenkäs'' he defines the ''Doppelgänger'' as the "people who see themselves."

Jean Paul was a lifelong defender of [[freedom of the press]] and his campaigns against censorship went beyond many of his contemporaries. In his ''Freiheitsbüchlein'' (1805), he maintains that books belong to humanity and should have the chance to have an impact on all times, not just the present moment, and therefore preventing a book from being published renders the censor a judge not just for contemporary society but for all future societies.<ref name="Ohe">{{cite book |last1=Ohe |first1=Werner von der |last2=McCarthy |first2=John A. |title=Zensur und Kultur: Zwischen Weimarer Klassik und Weimarer Republik mit einem Ausblick bis heute |date=2013 |publisher=Walter de Gruyter |pages=99–109}}</ref> Censorship is not feasible because it would be impossible to find a person able to fulfill the true requirements of the office.<ref name="Ohe" /> After the great achievements of the eighteenth century, the prospect of complete freedom of opinion, speech, and printing was real.<ref name="Ohe" /> Even under the tightened conditions of the Napoleonic occupation, Jean Paul continued to speak out in favor of reason, as in his ''Friedens-Predigt an Deutschland'' (1808).<ref name="Ohe" /> The last section of his ''Politische Fastenpredigten'' (1816) contains a warning to rulers that minds cannot be controlled, and that police action will only cause them to eventually explode like a champagne bottle.<ref name="Ohe" />

== Other ==
[[Rudolf Steiner]] edited a multi-volume collection of the works of Jean Paul.<ref>{{Cite book|url=https://books.google.com/books?id=iO2DCgAAQBAJ&q=rudolf+steiner+jean+paul&pg=PT42|title=Rudolf Steiner, Life and Work Volume 2 (1890-1900)|last=Selg|first=Peter|date=2015-08-01|publisher=SteinerBooks|isbn=9781621480877|language=en}}</ref> In published lectures, Steiner often mentioned the realization by the 7-year-old Jean Paul that he was an individual "Ego", expressed in Paul's surprise at understanding that "I am an I".

==Quotations==
* The long sleep of death closes our scars, and the short sleep of life our wounds. (''Der lange Schlaf des Todes schliesst unsere Narben zu, und der kurze des Lebens unsere Wunden'', ''Hesperus'', XX).

==Works==
[[File:Jean Paul – Titan vol 1 – BEIC 3988100.jpg|thumb|''Titan. 1'']]
* ''[[Abelard und Heloise]]'' 1781
* ''[[Grönländische Prozesse]]'' 1783–1784
* ''[[Auswahl aus des Teufels Papieren]]'' 1789
* ''[[Leben des vergnügten Schulmeisterlein Maria Wutz in Auenthal. Eine Art Idylle]]'' 1790
* ''[[Die unsichtbare Loge]]'' 1793
* ''[[Hesperus oder 45 Hundposttage(book)|Hesperus]]'' 1795
* ''[[Biographische Belustigungen]]'' 1796
* ''[[Leben des Quintus Fixlein]]'' 1796
* ''[[Siebenkäs]]'' 1796
* ''[[Der Jubelsenior]]'' 1797
* ''[[Das Kampaner Tal]]'' 1797
* ''[[Konjekturalbiographie]]'' 1798
* ''[[Des Luftschiffers Giannozzo Seebuch]]'' 1801
* ''[[Titan (Jean Paul novel)|Titan]]'' 1800–03
* ''[[Vorschule der Aesthetik]]'' 1804
* ''[[Flegeljahre]]'' (unfinished) 1804–05
* ''[[Freiheitsbüchlein'']] 1805
* ''[[Levana oder Erziehlehre]]'' 1807
* ''[[Dr. Katzenbergers Badereise]]'' 1809
* ''[[Des Feldpredigers Schmelzle Reise nach Flätz]]'' 1809
* ''[[Leben Fibels]]'' 1812
* ''[[Bemerkungen über uns närrische Menschen]]''
* ''[[Clavis Fichtiana]]'' (see also [[Johann Gottlieb Fichte]])
* ''[[Das heimliche Klaglied der jetzigen Männer]]''
* ''[[Der Komet]]'' 1820–1822
* ''[[Der Maschinenmann]]''
* ''[[Die wunderbare Gesellschaft in der Neujahrsnacht]]''
* ''[[Freiheits-Büchlein]]''
* ''[[Selberlebenbeschreibung]]'' posthum 1826
* ''[[Selina (Jean Paul novel)|Selina]]'' posthum 1827

===English translations===
Most of Richter's long novels were translated into English during the mid-nineteenth century. Several editions of translated passages from various works were also published:{{sfn|Americana staff|1920}}

* ''The Invisible Lodge'', trans. Charles T. Brooks, New York: Holt 1883
* ''Maria Wutz'' (various editions)
** ''Maria Wuz'', trans.  Francis and Rose Storr, ''Maria Wuz and Lorenz Stark'', London: Longmans, Green, & Co, 1881
** ''Maria Wutz'', trans. John D. Grayson, ''19th Century German Tales'', ed. Angel Flores, 1959, reissued 1966
** ''Maria Wutz'', trans. Erika Casey, ''The Jean Paul Reader'', Johns Hopkins U, 1990
** ''Maria Wutz'', trans. Francis and Rose Storr and Ruth Martin, Sublunary Editions, 2021<ref>{{Cite web|title=Maria Wutz|url=https://sublunaryeditions.com/empyrean/maria-wutz-jean-paul|url-status=live}}</ref>
* ''Hesperus'' by Charles Brooks (1864)
* ''Quintus Fixlein'', trans. [[Thomas Carlyle]], 1827
* ''Siebenkäs'' (two editions)
** ''Flower, Fruit, and Thorn Pieces'' trans. Edward Henry Noel (Boston: Ticknor and Fields, 1863)
** ''Flower, Fruit, and Thorn Pieces'' trans. [[Alexander Ewing (composer)|Alexander Ewing]] (1877)
* ''The Campaner Thal: or, Discourses on the Immortality of the Soul'' trans. Juliette Bauer (1848)
* ''Quintus Fixlein'' and ''Schmelzles Reise'' (1827), trans. [[Thomas Carlyle]]
* ''Titan'' by Charles Brooks (London: 1863; Boston: 1864)
* ''Horn of Oberon : Jean Paul Richter's School for Aesthetics'' trans. Margaret R Hale, Wayne State UP, 1973
* ''Walt and Vult'' [''Flegeljahre''] trans. [[Eliza Lee]] (1846)
* '''Army Chaplain Schmelzle's Journey'' (1827), by [[Thomas Carlyle]]
* ''Levana; or, the Doctrine of Education'', trans. A.H (1848,<ref>{{Cite book|last=RICHTER|first=Jean Paul Friedrich|url=https://books.google.com/books?id=GIFeAAAAcAAJ|title=Levana; or, the Doctrine of Education. Translated from the German [by A. H.].|date=1848|publisher=Longman & Company|language=en}}</ref> 1863,<ref>{{Cite book|last=RICHTER|first=Jean Paul Friedrich|url=https://books.google.com/books?id=YrpbAAAAcAAJ|title=Levana ... Translated from the German|date=1863|publisher=Ticknor & Fields|language=en}}</ref> 1884,<ref>{{Cite book|last=Richter|first=Jean Paul F.|url=https://books.google.com/books?id=up0IAAAAQAAJ|title=Levana; or, The doctrine of education, tr. [by A.H.]. Preceded by a short biogr. of the author [condensed from that of E. Förster] and his autobiography, a fragment|date=1880|language=en}}</ref> 1886,<ref>{{Cite book|last=Paul|first=Jean|url=https://books.google.com/books?id=GWIqAAAAYAAJ&dq=intitle:levana&pg=PA19|title=Levana, Or, The Doctrine of Education|date=1886|publisher=G. Bell|language=en}}</ref> 1890<ref>{{Cite book|last=Paul|first=Jean|url=https://books.google.com/books?id=IvdEAAAAIAAJ|title=Levana, Or, The Doctrine of Education|date=1890|publisher=D.C. Heath|language=en}}</ref>)
* ''The Death of an Angel & Other Pieces'' (1839)
* ''Reminiscences of the Best Hours of Life for the Hour of Death'' trans. Joseph Dowe (1841)

==Musical reception (selection)==
* [[Robert Schumann]]: ''[[Papillons]] pour le pianoforte seul'', 1832.
* Johann Friedrich Kittl: ''Wär’ ich ein Stern'', 1838.
* Robert Schumann: ''[[Blumenstück (Schumann)|Blumenstück]]'', 1839.
* Carl Grünbaum: ''Lied'' (Es zieht in schöner Nacht der Sternenhimmel), 1840.
* Ernst Friedrich Kauffmann: ''Ständchen nach Jean Paul'', 1848.
* [[Carl Reinecke]]: ''O wär’ ich ein Stern'' (from: Flegeljahre), 1850.
* [[Stephen Heller]]: ''Blumen-, Frucht- und Dornenstücke'' (Nuits blanches), 1850.
* Marta von Sabinin: ''O wär ich ein Stern'', 1855.
* Ernst Methfessel: ''An Wina'', 1866.
* [[Gustav Mahler]]: [[Symphony No. 1 (Mahler)|Symphony No. 1 "Titan"]], 1889.
* Ferdinand Heinrich Thieriot: ''Leben und Sterben des vergnügten Schulmeisterlein Wuz'', 1900.
* Hugo Leichtentritt: ''Grabschrift des Zephyrs'', 1910.
* [[Henri Sauguet]]: ''Polymetres'', 1936.
* Eduard Künnecke: ''Flegeljahre'', 1937.
* Karl Kraft: ''Fünf kleine Gesänge auf Verse des Jean Paul für Singstimme und Klavier'', 1960.
* Walter Zimmermann: ''Glockenspiel für einen Schlagzeuger'', 1983.
* [[Wolfgang Rihm]]: ''Andere Schatten'' (from: Siebenkäs), 1985.
* [[Oskar Sala]]: ''Rede des toten Christus vom Weltgebäude herab, dass kein Gott sei'', 1990.
* [[Iván Erőd]]: ''Blumenstück für Viola solo'', 1995.
* [[Thomas Beimel]]: ''Idyllen'', 1998/99.
* Christoph Weinhart: ''Albanos Traum'', 2006.
* [[Georg Friedrich Haas]]: ''Blumenstück'' (from: Siebenkäs), 2009.
* [[Ludger Stühlmeyer]]: ''Zum Engel der letzten Stunde'' (from: Das Leben des Quintus Fixlein), 2013.

==Notes==
{{Reflist}}

==References==
*{{Cite Americana | author=Americana staff |wstitle=Richter, Johann Paul Friedrich}}

;Attribution
* {{EB1911|wstitle=Richter, Johann Paul Friedrich}}

==Further reading==
* Fleming, Paul. ''The Pleasures of Abandonment: Jean Paul and the Life of Humor''. Würzburg: Königshausen & Neumann, 2006.

===Nineteenth-century works on Jean Paul===
Richter's ''Sämtliche Werke'' (''Complete Works'') appeared in 1826–1828 in 60 volumes, to which were added 5 volumes of ''[[Literarischer Nachlass]]'' (literary bequest) in 1836–1838; a second edition was published in 1840–1842 (33 volumes); a third in 1860–1862 (24 volumes). The last complete edition is that edited by [[Rudolf Gottschall|R. Gottschall]] (60 parts, 1879).{{sfn|Chisholm|1911}}

Editions of selected works appeared in 16 volumes (1865), in Kürschner's ''Deutsche Nationalliteratur'' (edited by P. Nerrlich, 6 vols, pp.&nbsp;388–487), &c. The chief collections of Richter's correspondence are:{{sfn|Chisholm|1911}}
* ''Jean Pauls Briefe an F. H. Jacobi'' (1828)
* ''Briefwechsel Jean Pauls mit seinem Freunde C. Otto'' (1829–33)
* ''Briefwechsel zwischen H. Voss und Jean Paul'' (1833)
* ''Briefe an eine Jugendfreundin'' (1858)
* P. Nerrlich, ''Jean Pauls Briefwechsel mit seiner Frau und seinem Freunde Otto'' (1902).

See further:{{sfn|Chisholm|1911}}
* The continuation of Richter's autobiography by C. Otto and E. Fürster (1826–33)
* H. Dring, ''J. P. F. Richter's Leben und Charakteristik'' (1830–32)
* [[Richard Otto Spazier]], ''JPF Richter: ein biographischer Commentar zu dessen Werken'' (5 vols, 1833)
* E. Förster, ''Denkwürdigkeiten aus dem Leben von J. P. F. Richter'' (1863)
* Paul Nerrlich, ''Jean Paul und seine Zeitgenossen'' (1876)
* J. Firmery, ''Étude sur la vie et les œuvres de J. P. F. Richter'' (1886)
* P. Nerrlich, ''Jean Paul, sein Leben und seine Werke'' (1889)
* [[Ferdinand Josef Schneider]], ''Jean Pauls Altersdichtung'' (1901); and ''Jean Pauls Jugend und erstes Auftreten in der Literatur'' (1906).
*Thomas Carlyle's two essays on Richter.
**{{Cite book |last=Carlyle |first=Thomas |title=[[Critical and Miscellaneous Essays]]: Volume I |publisher=[[Charles Scribner's Sons]] |year=1827 |series=The Works of Thomas Carlyle in Thirty Volumes |volume=XXVI |location=New York |publication-date=1904 |pages=1–25 |chapter=Jean Paul Friedrich Richter |author-link=Thomas Carlyle |chapter-url=https://archive.org/details/worksofthomascar26carliala/page/xii/mode/2up}}
**{{Cite book |last=Carlyle |first=Thomas |title=[[Critical and Miscellaneous Essays]]: Volume II |publisher=[[Charles Scribner's Sons]] |year=1830 |series=The Works of Thomas Carlyle in Thirty Volumes |volume=XXVII |location=New York |publication-date=1904 |pages=96–159 |chapter=Jean Paul Friedrich Richter Again |author-link=Thomas Carlyle |chapter-url=https://archive.org/details/worksofthomascar27carliala/page/96/mode/2up}}

==External links==
{{Wikiquote}}
{{Commons category|Jean Paul}}
{{Nuttall poster|Richter, Jean Paul Friedrich}}
* {{Gutenberg author |id=32901}}
* {{FadedPage|id=Richter, Johann Paul Friedrich|name=Jean Paul|author=yes}}
* {{Internet Archive author |sname=Jean Paul |sopt=t}}
* {{Librivox author |id=160}}
* {{OL author}}
* {{Zeno-Autor|Literatur/M/Jean+Paul}}
* [http://gutenberg.spiegel.de/autoren/jeanpaul.htm Jean Paul's works] at Projekt Gutenberg-DE (in German)
* {{Cite book|publisher=Bibliographisches Institut|last= Jean Paul|title= Titan. 2 |place= Leipzig und Wien|url= https://gutenberg.beic.it/webclient/DeliveryManager?pid=3259980}}
* {{Cite book|publisher=Bibliographisches Institut|last= Jean Paul|title= Titan. 1 |place= Leipzig und Wien|url= https://gutenberg.beic.it/webclient/DeliveryManager?pid=3988100}}
* {{Cite book|publisher=Bibliographisches Institut|last= Jean Paul|title= Jean Pauls Werke. 3 |place= Leipzig und Wien|url= https://gutenberg.beic.it/webclient/DeliveryManager?pid=3988987}}
* {{Cite book|publisher=Bibliographisches Institut|last= Jean Paul|title= Jean Pauls Werke. 4 |place= Leipzig und Wien|url= https://gutenberg.beic.it/webclient/DeliveryManager?pid=3990026}}
* {{Cite book|publisher=Bibliographisches Institut|last= Jean Paul|title= Jean Pauls Werke / herausgegeben von Rudolf Wustmann. 4 |place= Leipzig und Wien|url= https://gutenberg.beic.it/webclient/DeliveryManager?pid=3990908}}

{{Romanticism}}
{{German literature}}

{{Authority control}}

{{DEFAULTSORT:Jean Paul}}
[[Category:1763 births]]
[[Category:1825 deaths]]
[[Category:People from Wunsiedel]]
[[Category:People from the Principality of Bayreuth]]
[[Category:18th-century German novelists]]
[[Category:19th-century German novelists]]
[[Category:German male novelists]]
[[Category:Writers from Bavaria]]
[[Category:19th-century German male writers]]
[[Category:Blind people from Germany]]
[[Category:Deaths from edema]]
[[Category:18th-century German male writers]]"""
image_name = "Jean Paul – Titan vol 1 – BEIC 3988100.jpg"
image_name = "Jean-Paul-Denkmal (02).jpg"

image_name = image_name.replace("_", " ")
image_name = re.escape(image_name)
res = re.search(r"\[\[File:"+image_name+r"\s*\|(.*?)\]\]", test_text, flags=re.IGNORECASE)
res_all = re.findall(r"\[\[File:"+image_name+r"\s*\|(.*?)\]\]", test_text, flags=re.IGNORECASE)
res_all = re.finditer(r"\[\[File:"+image_name+r"\s*\|(?P<match>(.*?(?:\[\[.*?\]\])*.*?)*)\]\]", test_text, flags=re.IGNORECASE)
print("Match is:", res.groups())
for tmp in res_all:
    print("Match all is:", tmp.groups())
if "alt" in res.group(1):
    print("Contains alt already")
    # Handle replacement
    alt_pos = re.search(r"\|\s*alt=(.*?)[\]\|]", test_text, flags=re.IGNORECASE)
    print(alt_pos)
    print("match group", alt_pos.groups())
    print("Extracted position string:", test_text[alt_pos.start(1): alt_pos.end(1)])
    pass
else:
    # Add new alt element
    print("alt text not found")
    wikitext = test_text[:res.end() - 2] + f"|alt=marcel davis" + test_text[res.end() - 2:]
    print(wikitext)

print(test_text[res.start():res.end()])
