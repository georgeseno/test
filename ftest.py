import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BufferedInputFile 
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont
import io
from pol_test import PollingManager

TOKENS = ['PUT_YOUR_TOKEN_HERE']

async def getnewpicture(ishodnik, userforname, usersecondname):
 moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
 newdataforprint = moscow_time.strftime("%I : %M")
 userfirstname = userforname
 userseconame = usersecondname
 im1 = Image.open(ishodnik)
 im2 = Image.open(ishodnik)
 w, h = 220, 190
 shape = [(70, 40), (w - 75, h - 80)]
 mask_im = Image.new("L", im2.size, 0)
 draw = ImageDraw.Draw(mask_im)
 draw.ellipse(shape, fill=255)
 im1.paste(im2, (0, 0), mask_im)
 font = ImageFont.truetype("shrifts/HelveticaNeueCyr-Light.ttf", 30)
 font1 = ImageFont.truetype("shrifts/HelveticaNeueCyr-Bold.ttf", 23)
 drawer = ImageDraw.Draw(im1)
 drawer.text((170, 49), f"""{userfirstname} {userseconame}""", font=font, fill='black')
 drawer.text((342, 10), f"""{newdataforprint}""", font=font1, fill='black')
 im2.close()
 mask_im.close()
 buffer = io.BytesIO()
 im1.save(buffer, format='JPEG', quality=70)
 im1.close()
 return buffer.getbuffer()

logger = logging.getLogger(__name__)


async def mainmessages(message: types.Message, bot: Bot):
        newphoto = await getnewpicture(ishodnik='1.png', userforname=1, usersecondname=1)
        datphoto = await getnewpicture(ishodnik='2.png', userforname=1, usersecondname=1)
        mediagroup = [types.InputMediaPhoto(media=BufferedInputFile(newphoto, '2')), types.InputMediaPhoto(media=BufferedInputFile(datphoto, '2'))]
        await bot.send_media_group(message.from_user.id,
          mediagroup
        )




async def main():
    
    bots = [Bot(token, parse_mode='HTML') for token in TOKENS]
    dp = Dispatcher()    
    dp.message.register(mainmessages, text='1') 
    
    polling_manager = PollingManager()
    for bot in bots:
        await bot.get_updates(offset=-1)
    await dp.start_polling(*bots, dp_for_new_bot=dp, polling_manager=polling_manager)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Exit")
