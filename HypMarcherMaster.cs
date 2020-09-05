//Based on David Kuri's "GPU Ray Tracing in Unity" Tutorial (http://three-eyed-games.com/2018/05/03/gpu-ray-tracing-in-unity-part-1/)


using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HypMarcherMaster : MonoBehaviour
{

    //A reference to the compute shader that describes the actual computation
    public ComputeShader HypMarcherShader;

    public Texture _SkyboxTexture;

    //The texture data being manipulated by the shader
    private RenderTexture _target;

    
    private Camera _camera;

    private void Awake() {
        _camera = GetComponent<Camera>();
    }

    
    private void SetShaderParameters() 
    {
        HypMarcherShader.SetMatrix("_CameraToWorld", _camera.cameraToWorldMatrix);
        HypMarcherShader.SetMatrix("_CameraInverseProjection", _camera.projectionMatrix.inverse);
        HypMarcherShader.SetTexture(0, "_SkyboxTexture", _SkyboxTexture);
    }


    


    //Method that is called on render, supplied with a source texture and a destination. we call Render() on the destination to render the image
    private void OnRenderImage(RenderTexture source, RenderTexture destination) {
        SetShaderParameters(); //This sends the camera's matricies into the compute shader so it can use it for making rays, along with lots of other information for other things
        Render(destination);
    }


    //Releases the current _target texture if it exists, and assigns it a new texture that is the size of the screen
    private void InitRenderTexture() {
              
        if (_target == null || _target.width != Screen.width || _target.height != Screen.height) {
            if(_target != null) {
                _target.Release();
            }

            _target = new RenderTexture(Screen.width, Screen.height, 0, RenderTextureFormat.ARGBFloat, RenderTextureReadWrite.Linear);
            _target.enableRandomWrite = true;
            _target.Create();
        }

        
    }

    //Breaks the texture into groups and tells the compute shader what to do
    private void Render(RenderTexture destination) {

        InitRenderTexture();

        HypMarcherShader.SetTexture(0, "Result", _target);
        int threadGroupsX = Mathf.CeilToInt(Screen.width / 8.0f);
        int threadGroupsY = Mathf.CeilToInt(Screen.height / 8.0f);
        HypMarcherShader.Dispatch(0, threadGroupsX, threadGroupsY, 1);
        Graphics.Blit(_target, destination);
    }

    private void Update() 
    {


    }




}
