from blog.models.formalMethod import FormalMethod

formalmethod = FormalMethod(name='LTL')
formalmethod.save()
formalmethod = FormalMethod(name='CTL')
formalmethod.save()
formalmethod = FormalMethod(name='PPTL')
formalmethod.save()