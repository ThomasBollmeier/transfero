import re

class Scanner(object):
    
    WHITESPACE = "__WSPACE__"
    COMMENT = "__COMMENT__"
    
    def __init__(self, case_sensitive=True, wspace=[" ", "\t", "\r", "\n"]):
        self._patterns = []
        self._case_sensitive = case_sensitive
        self._set_wspace_chars(wspace)
        
    def _set_wspace_chars(self, chars):
        self._wspace_pattern = "[" + "".join(chars) + "]"
        self._patterns.append((self.WHITESPACE, re.compile("^(" + self._wspace_pattern + ")")))
        
    def add_token(self, name, pattern):
        self._patterns.append((name, re.compile("^(" + pattern + ")")))
        return self
        
    def add_keyword(self, keyword):
        name = keyword.upper()
        if self._case_sensitive:
            kw = keyword
        else:
            kw = ""
            for ch in keyword:
                kw += "({}|{})".format(ch.lower(), ch.upper())
        pattern = "^(" + kw + ")(?:" + self._wspace_pattern + "|\Z)"
        self._patterns.insert(0, (name, re.compile(pattern)))
        return self
    
    def add_comment(self, start, end):
        pattern = self._regex_escape(start)
        pattern += "({})*".format(self._not_pattern(end))
        pattern += self._regex_escape(end)
        pattern = "(" + pattern + ")"
        self._patterns.insert(0, (self.COMMENT, re.compile(pattern)))
        return self
        
    def _regex_escape(self, s):
        ret = ""
        for ch in s:
            if ch in ["*", "+", "?", "\\", "(", ")"]:
                ret += "\\"
            ret += ch
        return ret
    
    def _not_pattern(self, s):
        ret = ""
        left = ""
        right = s
        while right:
            if left:
                ret += "|({}[^{}]?)".format(self._regex_escape(left), right[0])
            else:
                ret += "[^{}]".format(right[0])
            left += right[0]
            right = right[1:]
        return ret
    
    def find_tokens(self, source):
        tokens = []
        remaining = source
        while remaining:
            for name, regex in self._patterns:
                m = regex.match(remaining)
                if m:
                    text = m.group(1)
                    if name not in [self.WHITESPACE, self.COMMENT]:
                        tokens.append((name, text))
                    remaining = remaining[len(text):]
                    break
            else:
                break
        if remaining:
            raise Exception("Code could not be resolved: {}".format(remaining))
        return tokens