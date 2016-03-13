# Author: Joshua Chen
# Date: 2016-03-13
# Location: Shenzhen
# Description: step module

import interact

class QuitException(Exception): pass

class Step:
    """ Represents one single step of a procedure.
    """

    # Wait for user confirmation before next step
    wait = True

    # return codes
    NEXT      = 11
    PREVIOUS  = 12
    STARTOVER = 13
    END       = 14
    QUIT      = 15
    HELP      = 16

    def __init__(self, desc='', info='', help='', **kargs):
        self.desc   = desc
        self.info   = info
        self.help   = help
        self.childs = []
        self.kargs  = kargs

    def add(self, *pargs, **kargs):
        """ Add a sub step
        """
        subStep = Step(*pargs, **kargs)
        self.childs.append(subStep)
        return subStep

    def show(self):
        """ Show the information of the step itself
        """
        text = self.desc
        if self.info:
            text += ('\n' + self.info)
        print(text)
        if self.childs:     # no actions for a parent step
            return Step.NEXT
        cmds = 'npseqh'
        while True:
            uin = interact.pickValue('>> ', default='n', values=list(cmds))
            if uin == 'n':
                return Step.NEXT
            elif uin == 'p':
                return Step.PREVIOUS
            elif uin == 's':
                return Step.STARTOVER
            elif uin == 'e':
                return Step.END
            elif uin == 'q':
                return Step.QUIT
            elif uin == 'h':
                text = self.help
                if not text:
                    print('no help available')
                else:
                    print('--- help message ---')
                    print(text)

    def play(self):
        """ Show the step itself, and its child
        steps one by one if there is any.
        """
        code     = self.show()
        subSteps = self.childs
        total    = len(subSteps)
        if not total:
            return code
        curPos = 0
        while True:
            subStep = subSteps[curPos]
            code    = subStep.play()
            if code == Step.NEXT:
                curPos = self.next(curPos)
            elif code == Step.END:
                return Step.NEXT    # to the next in the parent
            elif code == Step.PREVIOUS:
                curPos = self.previous(curPos)
            elif code == Step.STARTOVER:
                curPos = 0
            elif code == Step.QUIT:
                self.quit()
            if curPos >= total:
                return Step.NEXT    # to the next in the parent

    def next(self, curPos, n=1):
        """ Return the index of the next 'n' child step
        in all the child steps.
        """
        newPos = curPos + n
        total  = len(self.childs)
        if newPos >= total:
            newPos = total
        return newPos

    def previous(self, curPos, n=1):
        """ Return the index of the previous 'n' child step
        in all the child steps.
        """
        newPos = curPos - n
        if newPos < 0:
            newPos = 0
        return newPos

    def quit(self):
        """ Raise an QuitException exception.
        """
        raise QuitException
