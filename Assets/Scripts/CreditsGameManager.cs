using UnityEngine;
using UnityEngine.UI;

public class CreditsGameManager : MonoBehaviour
{
    public Text highScoreText;  //high score text
    public Text scoreText;      //score text

    void Update()
    {
        scoreText.text = PlayerPrefs.GetInt("Score", 0).ToString();             //get score text from score
        highScoreText.text = PlayerPrefs.GetInt("Highscore", 0).ToString();     //get high score text from highscore
    }
}
