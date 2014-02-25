import codecs
import copy
from functools import total_ordering

@total_ordering
class Member:
  def __init__(self, name, title, officehours):
    self.name = name
    self.sort_name = name.split()[-1]
    self.title = title
    self.officehours = officehours

  @staticmethod
  def from_file(f):
    name = f.readline()
    if not name:
      return
    name = name.strip()
    title = f.readline().strip()
    officehours = f.readline().strip()
    f.readline()
    return Member(name, title, officehours)

  def __eq__(self, other):
    return self.name == other.name

  def __lt__(self, other):
    return self.sort_name < other.sort_name

  def __str__(self):
    return self.name

  def __repr__(self):
    return 'Member "%s"' % self.name
    

class Template:
  def __init__(self, filename=None, template=None):
    if filename is not None:
      with codecs.open(filename, encoding='utf-8') as f:
        self.template = f.read()
    else:
      self.template = template

  def render(self, m1, m2):
    template = self.template
    for i, member in enumerate([m1, m2]):
      template = template\
          .replace("player%d" % i, member.name) \
          .replace("title%d" % i, member.title) \
          .replace("officehours%d" % i, member.officehours)

    return Template(template=template)
  
  def save(self, filename):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
      f.write(self.template)

def read_members(filename):
  members = []
  with codecs.open(filename, encoding='utf-8') as f:
    member = Member.from_file(f)
    while member:
      members.append(member)
      member = Member.from_file(f)
  return members


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 3:
    print("Usage:")
    print("python create_signs.py template.svg members.txt")
  else:
    template = Template(sys.argv[1])
    members = read_members(sys.argv[2])
    members.sort()

    if len(members) % 2 == 1:
      members.append(Member("", "", ""))

    for i in range(0, len(members), 2):
      m = members[i:i+2]
      filename = '%s_%s.svg' % (
          m[0].name.replace(" ", "_"),
          m[1].name.replace(" ", "_"), 
      )
      template.render(*m).save(filename)
