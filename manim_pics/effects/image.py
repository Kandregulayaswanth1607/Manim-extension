"""Cinematic raster effects for ImageAsset (Pillow/NumPy only)."""
from __future__ import annotations
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


def _asset(asset, pixels, label):
    from ..core.asset import ImageAsset
    return ImageAsset(pixels, metadata=asset.metadata, history=asset.history + [label])


def vignette(asset, strength=0.65, softness=0.55):
    """Darken image edges with a smooth elliptical vignette. strength in [0,1]."""
    if not 0 <= strength <= 1 or not 0 < softness <= 1: raise ValueError('strength must be 0..1 and softness 0..1')
    a=asset.pixels.copy(); h,w=a.shape[:2]
    y,x=np.ogrid[-1:1:complex(h),-1:1:complex(w)]
    r=np.sqrt(x*x+y*y); edge=np.clip((r-softness)/(1-softness),0,1)
    factor=1-strength*edge*edge*(3-2*edge)
    a[:,:,:3]=np.clip(a[:,:,:3].astype(float)*factor[:,:,None],0,255).astype('uint8')
    return _asset(asset,a,f'vignette({strength},{softness})')


def film_grain(asset, amount=0.08, seed=0, monochrome=True):
    """Add deterministic film grain; amount is noise standard deviation / 255."""
    if amount < 0 or amount > 1: raise ValueError('amount must be between 0 and 1')
    a=asset.pixels.copy(); rng=np.random.default_rng(seed); h,w=a.shape[:2]
    noise=rng.normal(0,255*amount,(h,w,1 if monochrome else 3))
    if monochrome: noise=np.repeat(noise,3,axis=2)
    a[:,:,:3]=np.clip(a[:,:,:3].astype(float)+noise,0,255).astype('uint8')
    return _asset(asset,a,f'film_grain({amount})')


def bloom(asset, radius=12, intensity=0.8, threshold=190):
    """Soft highlight bloom composited over the source."""
    if radius < 0 or intensity < 0: raise ValueError('radius and intensity must be non-negative')
    im=asset.to_pillow(); rgb=np.asarray(im.convert('RGB')).astype(float)
    lum=rgb.mean(axis=2); mask=(lum>=threshold).astype('uint8')*255
    glow=Image.fromarray(np.dstack([rgb.astype('uint8'),mask]),'RGBA').filter(ImageFilter.GaussianBlur(radius))
    out=Image.blend(im,Image.alpha_composite(im,glow),min(1.0,intensity))
    return _asset(asset,np.asarray(out).copy(),f'bloom({radius},{intensity})')


def chromatic_aberration(asset, offset=4):
    """Separate RGB channels horizontally for a lens-fringe effect."""
    if offset < 0: raise ValueError('offset must be non-negative')
    a=asset.pixels.copy(); out=a.copy();
    out[:,:,0]=np.roll(a[:,:,0],offset,axis=1); out[:,:,2]=np.roll(a[:,:,2],-offset,axis=1)
    return _asset(asset,out,f'chromatic_aberration({offset})')


def scanlines(asset, spacing=3, opacity=0.22):
    """Apply subtle horizontal CRT scanlines."""
    if spacing < 1 or not 0 <= opacity <= 1: raise ValueError('spacing >= 1 and opacity 0..1 required')
    a=asset.pixels.copy(); a[::spacing,:,:3]=(a[::spacing,:,:3].astype(float)*(1-opacity)).astype('uint8')
    return _asset(asset,a,f'scanlines({spacing},{opacity})')


def color_grade(asset, contrast=1.08, saturation=1.12, brightness=1.0, tint=(1.0,0.96,0.88)):
    """Apply a simple cinematic contrast/saturation/brightness and RGB tint."""
    im=asset.to_pillow().convert('RGB')
    im=ImageEnhance.Contrast(im).enhance(contrast); im=ImageEnhance.Color(im).enhance(saturation); im=ImageEnhance.Brightness(im).enhance(brightness)
    a=np.asarray(im).astype(float)*np.asarray(tint).reshape(1,1,3)
    rgba=np.dstack([np.clip(a,0,255).astype('uint8'),asset.pixels[:,:,3]])
    return _asset(asset,rgba,'color_grade')


def glitch(asset, amount=0.12, slices=12, seed=0, rgb_shift=3):
    """Digital horizontal-slice displacement with subtle RGB separation."""
    if not 0 <= amount <= 1 or slices < 1 or rgb_shift < 0: raise ValueError('invalid glitch parameters')
    a=asset.pixels.copy(); h,w=a.shape[:2]; rng=np.random.default_rng(seed)
    band=max(1,h//slices)
    for y in range(0,h,band):
        if rng.random()<amount:
            end=min(h,y+band); shift=int(rng.integers(-max(1,w//12),max(2,w//12+1)))
            a[y:end]=np.roll(a[y:end],shift,axis=1)
    if rgb_shift:
        base=a.copy(); a[:,:,0]=np.roll(base[:,:,0],rgb_shift,axis=1); a[:,:,2]=np.roll(base[:,:,2],-rgb_shift,axis=1)
    return _asset(asset,a,f'glitch({amount},{slices})')
