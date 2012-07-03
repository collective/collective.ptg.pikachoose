from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery import PTGMessageFactory as _
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema


class IPikachooseDisplaySettings(IBaseSettings):
    pikachoose_width = schema.Int(
        title=_(u"label_pikachoose_width",
            default=u"Width of the gallery in pixels"),
        default=600,
        min=10)
    pikachoose_height = schema.Int(
        title=_(u"label_pikachoose_height",
            default=u"Height of the gallery in pixels"),
        default=350,
        min=10)
    pikachoose_backgroundcolor = schema.Choice(
        title=_(u"label_pikachoose_backgroundcolor",
                default=u"backgroundcolor"),
        default='222',
        vocabulary=SimpleVocabulary([
            SimpleTerm('222', '222',
                _(u"label_backgroundcolors", default=u"Dark")),
            SimpleTerm('DDD', 'DDD',
                _(u"label_backgroundcolors2", default=u"Grey")),
            SimpleTerm('f6f6f6', 'f6f6f6',
                _(u"label_backgroundcolors3", default=u"Offwhite")),
            SimpleTerm('FFF', 'FFF',
                _(u"label_backgroundcolors4", default=u"White")
            )
        ]))
    pikachoose_showtooltips = schema.Bool(
        title=_(u"label_pikachoose_tooltip", default=u"Show tooltip"),
        default=False)
    pikachoose_showcaption = schema.Bool(
        title=_(u"label_pikachoose_caption", default=u"Show caption"),
        default=True)
    pikachoose_vertical = schema.Bool(
        title=_(u"label_pikachoose_vertical", default=u"Vertical"),
        default=False)
    pikachoose_transition = schema.Choice(
        title=_(u"label_pikachoose_transition", default=u"Transition"),
        default=4,
        vocabulary=SimpleVocabulary([
            SimpleTerm(1, 1,
                _(u"label_transitions", default=u"Full frame cross fade")),
            SimpleTerm(2, 2,
                _(u"label_transitions2", default=u"Paneled fold out")),
            SimpleTerm(3, 3,
                _(u"label_transitions3", default=u"Horizontal blinds")),
            SimpleTerm(4, 4,
                _(u"label_transitions4", default=u"Vertical blinds")),
            SimpleTerm(5, 5,
                _(u"label_transitions5", default=u"Small box random fades")),
            SimpleTerm(6, 6,
                _(u"label_transitions6", default=u"Full image blind slide")),
            SimpleTerm(0, 0,
                _(u"label_transitions7", default=u"Fade out then fade in")
            )
        ]))


class PikachooseDisplayType(BaseDisplayType):

    name = u"pikachoose"
    schema = IPikachooseDisplaySettings
    description = _(u"label_pikachoose_display_type",
        default=u"Pikachoose")
    staticFilesRelative = '++resource++ptg.pikachoose'

    def javascript(self):
        return u"""
<script type="text/javascript"
src="%(portal_url)s/++resource++ptg.pikachoose/assets/js/jquery.pikachoose.js">
    </script>
<script type="text/javascript"
src="%(portal_url)s/++resource++ptg.pikachoose/assets/js/jquery.jcarousel.min.js">
    </script>
<script language="javascript">
$(document).ready(function(){
    var preventStageHoverEffect = function(self){
        self.wrap.unbind('mouseenter').unbind('mouseleave');
        self.imgNav.append('<a class="tray"></a>');
        self.imgNav.show();
        self.hiddenTray = true;
        self.imgNav.find('.tray').bind('click',function(){
            if(self.hiddenTray){
                var selector = '.jcarousel-container.jcarousel-container-';
                self.list.parents(selector + 'vertical').animate(
                    {height:"%(verticalheight)ipx"});
                self.list.parents(selector + 'horizontal').animate(
                    {height:"80px"});
            }else{
                self.list.parents('.jcarousel-container').animate(
                    {height:"1px"});
            }
            self.hiddenTray = !self.hiddenTray;
        });
    }
    $("#pikame").PikaChoose({
        bindsFinished: preventStageHoverEffect,
        transition:[%(transition)i],
        animationSpeed: %(duration)i,
        fadeThumbsIn: %(fadethumbsin)s,
        speed: %(speed)s,
        carouselVertical: %(vertical)s,
        showCaption: %(showcaption)s,
        thumbOpacity: 0.4,
        autoPlay: %(autoplay)s,
        carousel: 'false',
        showTooltips: %(showtooltips)s });
});
</script>
""" % {
        'portal_url': self.portal_url,
        'duration': self.settings.duration,
        'speed': self.settings.delay,
        'transition': self.settings.pikachoose_transition,
        'autoplay': jsbool(self.settings.timed),
        'showcaption': jsbool(self.settings.pikachoose_showcaption),
        'showtooltips': jsbool(self.settings.pikachoose_showtooltips),
        'carousel': jsbool(self.settings.pikachoose_showcarousel),
        'vertical': jsbool(self.settings.pikachoose_vertical),
        'thumbopacity': 0.4,
        'fadethumbsin': 'false',
        'verticalheight': self.settings.pikachoose_height - 18,
    }

    def css(self):
        return u"""
        <style>
.pikachoose,
.pika-stage {
   height: %(height)ipx;
   width: %(width)ipx;
}

.pika-stage {
   height: %(height)ipx;
   width: %(width)ipx;
}

.pika-stage, .pika-thumbs li{
    background-color: #%(backgroundcolor)s;
}

.jcarousel-skin-pika .jcarousel-container-vertical,
.jcarousel-skin-pika .jcarousel-clip-vertical{
   height: %(lowerheight)ipx;
</style>
<link rel="stylesheet" type="text/css" href="%(base_url)s/css/style.css"/>
""" % {
        'height': self.settings.pikachoose_height,
        'width': self.settings.pikachoose_width,
        'lowerheight': self.settings.pikachoose_height - 18,
        'backgroundcolor': self.settings.pikachoose_backgroundcolor,
        'base_url': self.staticFiles
    }
PikachooseSettings = createSettingsFactory(PikachooseDisplayType.schema)
