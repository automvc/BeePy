"""    
Corresponding Java type ORM tool,
JAVA ORM Bee:

       maven:
       <dependency>
          <groupId>org.teasoft</groupId>
          <artifactId>bee-all</artifactId>
          <version>2.4.2</version>
        </dependency>
        
        Gradle(Short):
        implementation 'org.teasoft:bee-all:2.4.2'
        
        note:the version can change to newest.

"""
from bee.version import Version


Version.printversion()
